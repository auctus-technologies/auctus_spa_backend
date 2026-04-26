import base64
import os
import tempfile
import numpy as np
import cv2
from datetime import date, time, datetime
from typing import Optional, List
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from . import api
from main.models import Attendance, User, EmployeeProfile
from .schemas import (
    AttendanceCreateSchema, AttendanceUpdateSchema, AttendanceResponse, AttendanceStatsSchema,
    MarkFaceAttendanceSchema, MarkFaceAttendanceResponse, FaceAttendanceErrorResponse,
)


# ── /attendance  (collection) ─────────────────────────────────────────────────

@api.get("/attendance", response=List[AttendanceResponse])
def list_attendance(request, user_id: Optional[int] = None, date_from: Optional[date] = None, date_to: Optional[date] = None):
    queryset = Attendance.objects.select_related('user')
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    return [
        AttendanceResponse(
            id=a.id,
            user_id=a.user.id,
            user_name=a.user.name,
            date=a.date,
            check_in_time=a.check_in_time.strftime("%H:%M") if a.check_in_time else None,
            check_out_time=a.check_out_time.strftime("%H:%M") if a.check_out_time else None,
            status=a.status,
        )
        for a in queryset.order_by('-date', '-check_in_time')
    ]


@api.post("/attendance", response=AttendanceResponse)
def create_attendance(request, payload: AttendanceCreateSchema):
    user = get_object_or_404(User, id=payload.user_id)
    check_in = time.fromisoformat(payload.check_in_time) if payload.check_in_time else None
    check_out = time.fromisoformat(payload.check_out_time) if payload.check_out_time else None
    status = getattr(payload, 'status', 'present') or 'present'
    attendance = Attendance.objects.create(
        user=user, date=payload.date,
        check_in_time=check_in, check_out_time=check_out, status=status,
    )
    return AttendanceResponse(
        id=attendance.id, user_id=user.id, user_name=user.name, date=attendance.date,
        check_in_time=attendance.check_in_time.strftime("%H:%M") if attendance.check_in_time else None,
        check_out_time=attendance.check_out_time.strftime("%H:%M") if attendance.check_out_time else None,
        status=attendance.status,
    )


# ── /attendance/<literal sub-paths>  — MUST come before /{attendance_id} ─────

@api.get("/attendance/stats/today", response=AttendanceStatsSchema)
def get_today_attendance_stats(request):
    today = date.today()
    total_employees = User.objects.filter(role='employee').count()
    present_today = Attendance.objects.filter(date=today).count()
    late_time = time(9, 30)
    late_checkins = Attendance.objects.filter(date=today, check_in_time__gt=late_time).count()
    return AttendanceStatsSchema(
        total_employees=total_employees,
        present_today=present_today,
        leave_today=total_employees - present_today,
        late_checkins=late_checkins,
    )


@api.post("/attendance/check-in", response=AttendanceResponse)
def check_in(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    today = date.today()
    current_time = datetime.now().time()
    attendance, created = Attendance.objects.get_or_create(
        user=user, date=today,
        defaults={'check_in_time': current_time, 'status': 'present'},
    )
    return AttendanceResponse(
        id=attendance.id, user_id=user.id, user_name=user.name, date=attendance.date,
        check_in_time=attendance.check_in_time.strftime("%H:%M") if attendance.check_in_time else None,
        check_out_time=attendance.check_out_time.strftime("%H:%M") if attendance.check_out_time else None,
        status=attendance.status,
    )


@api.post("/attendance/check-out", response=AttendanceResponse)
def check_out(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    today = date.today()
    current_time = datetime.now().time()
    attendance = get_object_or_404(Attendance, user=user, date=today)
    attendance.check_out_time = current_time
    attendance.save()
    return AttendanceResponse(
        id=attendance.id, user_id=user.id, user_name=user.name, date=attendance.date,
        check_in_time=attendance.check_in_time.strftime("%H:%M") if attendance.check_in_time else None,
        check_out_time=attendance.check_out_time.strftime("%H:%M"),
        status=attendance.status,
    )


@api.post(
    "/attendance/mark-face",
    response={
        200: MarkFaceAttendanceResponse,
        400: FaceAttendanceErrorResponse,
        404: FaceAttendanceErrorResponse,
        409: FaceAttendanceErrorResponse,
    },
)
def mark_face_attendance(request, payload: MarkFaceAttendanceSchema):
    """Mark attendance via face recognition (DeepFace + ArcFace)."""

    # ── 1. Look up employee by phone ──────────────────────────────────────
    phone = payload.phone.strip()
    profile = (
        EmployeeProfile.objects
        .select_related('user')
        .filter(phone__in=[phone, f'+91{phone}', f'91{phone}'])
        .first()
    )
    if not profile:
        return 404, {"error": "user_not_found", "message": "User not found"}

    user = profile.user

    # ── 2. Ensure face embedding was stored at registration ───────────────
    if not user.avatar_embedding:
        return 400, {"error": "no_avatar", "message": "Profile photo not set. Contact admin."}

    # ── 3. Decode webcam photo ────────────────────────────────────────────
    try:
        photo_bytes = base64.b64decode(payload.photo_base64)
    except Exception:
        return 400, {"error": "invalid_photo", "message": "Invalid photo data"}

    # ── 4. Webcam-only DeepFace inference; avatar embedding from DB ───────
    tmp_path = None
    face_verified = False
    try:
        from deepface import DeepFace

        # CLAHE preprocessing to handle uneven office lighting
        nparr = np.frombuffer(photo_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_bgr is not None:
            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            enhanced = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
        else:
            enhanced = None

        # mkstemp: fd closed before cv2 writes (Windows file-locking fix)
        tmp_fd, tmp_path = tempfile.mkstemp(suffix='.jpg')
        os.close(tmp_fd)
        if enhanced is not None:
            cv2.imwrite(tmp_path, enhanced, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            with open(tmp_path, 'wb') as f:
                f.write(photo_bytes)

        webcam_res = DeepFace.represent(
            img_path=tmp_path,
            model_name="ArcFace",
            detector_backend="opencv",
            enforce_detection=False,
            align=True,
        )
        webcam_emb = np.array(webcam_res[0]["embedding"])
        avatar_emb = np.array(user.avatar_embedding)

        cosine_dist = 1.0 - float(
            np.dot(avatar_emb, webcam_emb) /
            (np.linalg.norm(avatar_emb) * np.linalg.norm(webcam_emb))
        )
        match_confidence = round((1.0 - cosine_dist) * 100, 1)
        face_verified = match_confidence >= 40.0
        print(f"[face] user={user.id} match={match_confidence}% verified={face_verified}")

    except ImportError:
        return 400, {"error": "server_error", "message": "Face recognition library not installed"}
    except Exception:
        import traceback; traceback.print_exc()
        face_verified = False
        match_confidence = 0.0
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if not face_verified:
        return 400, {"error": "face_not_recognized", "message": "Your face is not recognized"}

    # ── 5. Create / fetch today's attendance record ───────────────────────
    today = date.today()
    current_time = datetime.now().time()
    address = (payload.address or "").strip()

    attendance, _ = Attendance.objects.get_or_create(
        user=user, date=today,
        defaults={"status": "present"},
    )

    # ── 6. Check-in or check-out ──────────────────────────────────────────
    if not attendance.check_in_time:
        action = "check_in"
        attendance.check_in_time = current_time
        attendance.check_in_address = address
        attendance.status = "present"
        attendance.check_in_photo.save(
            f"checkin_{user.id}_{today}.jpg", ContentFile(photo_bytes), save=False
        )
        attendance.save()

    elif not attendance.check_out_time:
        action = "check_out"
        attendance.check_out_time = current_time
        attendance.check_out_address = address
        attendance.check_out_photo.save(
            f"checkout_{user.id}_{today}.jpg", ContentFile(photo_bytes), save=False
        )
        attendance.save()

    else:
        return 409, {
            "error": "already_completed",
            "message": "You have already checked in and out for today.",
        }

    # ── 7. Build response ─────────────────────────────────────────────────
    def fmt_time(t):
        return t.strftime("%I:%M %p") if t else None

    date_str = today.strftime("%d %B %Y")
    designation_label = dict(EmployeeProfile.DESIGNATION_CHOICES).get(
        profile.designation, profile.designation
    )
    department_label = dict(EmployeeProfile.DEPARTMENT_CHOICES).get(
        profile.department, profile.department
    )

    return 200, {
        "success": True,
        "action": action,
        "user_name": user.name,
        "employee_id": profile.employee_id,
        "designation": designation_label,
        "department": department_label,
        "match_confidence": match_confidence,
        "check_in_time": fmt_time(attendance.check_in_time),
        "check_in_date": date_str,
        "check_in_address": attendance.check_in_address,
        "check_out_time": fmt_time(attendance.check_out_time) if action == "check_out" else None,
        "check_out_date": date_str if action == "check_out" else None,
        "check_out_address": attendance.check_out_address if action == "check_out" else None,
    }


# ── /attendance/{id}  (parameterized — must come last) ───────────────────────

@api.get("/attendance/{attendance_id}", response=AttendanceResponse)
def get_attendance(request, attendance_id: int):
    attendance = get_object_or_404(Attendance.objects.select_related('user'), id=attendance_id)
    return AttendanceResponse(
        id=attendance.id, user_id=attendance.user.id, user_name=attendance.user.name,
        date=attendance.date,
        check_in_time=attendance.check_in_time.strftime("%H:%M") if attendance.check_in_time else None,
        check_out_time=attendance.check_out_time.strftime("%H:%M") if attendance.check_out_time else None,
        status=attendance.status,
    )


@api.put("/attendance/{attendance_id}", response=AttendanceResponse)
def update_attendance(request, attendance_id: int, payload: AttendanceUpdateSchema):
    attendance = get_object_or_404(Attendance.objects.select_related('user'), id=attendance_id)
    if payload.check_in_time is not None:
        attendance.check_in_time = time.fromisoformat(payload.check_in_time) if payload.check_in_time else None
    if payload.check_out_time is not None:
        attendance.check_out_time = time.fromisoformat(payload.check_out_time) if payload.check_out_time else None
    if payload.status:
        attendance.status = payload.status
    attendance.save()
    return AttendanceResponse(
        id=attendance.id, user_id=attendance.user.id, user_name=attendance.user.name,
        date=attendance.date,
        check_in_time=attendance.check_in_time.strftime("%H:%M") if attendance.check_in_time else None,
        check_out_time=attendance.check_out_time.strftime("%H:%M") if attendance.check_out_time else None,
        status=attendance.status,
    )


@api.delete("/attendance/{attendance_id}")
def delete_attendance(request, attendance_id: int):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.delete()
    return {"success": True, "message": "Attendance record deleted successfully"}
