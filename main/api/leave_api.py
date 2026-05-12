from typing import List
from django.shortcuts import get_object_or_404
from ninja import File, Form
from ninja.files import UploadedFile
from . import api
from main.models import LeaveRequest, LeaveDocument, User, Notification
from .schemas import LeaveResponse, LeaveDocumentSchema, ChoiceItem, LeaveTypesResponse


def _notify(users, title, message, notif_type):
    Notification.objects.bulk_create([
        Notification(user=u, title=title, message=message, notif_type=notif_type)
        for u in users
    ])


def _build_response(leave: LeaveRequest) -> LeaveResponse:
    documents = [
        LeaveDocumentSchema(
            id=doc.id,
            file_url=f"/media/{doc.file.name}",
            uploaded_at=doc.uploaded_at
        )
        for doc in leave.documents.all()
    ]
    # Get employee_id from user profile if exists
    employee_id = None
    try:
        employee_id = leave.user.profile.employee_id
    except:
        pass
    return LeaveResponse(
        id=leave.id,
        user_id=leave.user.id,
        user_name=leave.user.name,
        employee_id=employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status=leave.status,
        documents=documents,
        applied_date=leave.applied_date,
    )


@api.get("/leave-requests", response=List[LeaveResponse])
def list_leave_requests(request):
    """Admins see all requests; employees see only their own."""
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)

    if request.user.role == 'admin':
        qs = LeaveRequest.objects.select_related('user').prefetch_related('documents').all()
    else:
        qs = LeaveRequest.objects.select_related('user').prefetch_related('documents').filter(user=request.user)

    return [_build_response(l) for l in qs]


@api.post("/leave-requests", response=LeaveResponse)
def create_leave_request(
    request,
    leave_type: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    reason: str = Form(...),
    documents: List[UploadedFile] = File(None),
):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)

    leave = LeaveRequest(
        user=request.user,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
    )
    leave.save()

    if documents:
        for doc in documents:
            LeaveDocument.objects.create(leave_request=leave, file=doc)

    admins = User.objects.filter(role='admin', is_active=True)
    _notify(
        admins,
        title=f'Leave Request: {request.user.name}',
        message=f'{request.user.name} has submitted a {leave.get_leave_type_display()} request ({leave.start_date} – {leave.end_date}).',
        notif_type='leave_submitted',
    )

    return _build_response(leave)



@api.put("/leave-requests/{leave_id}/approve", response=LeaveResponse)
def approve_leave_request(request, leave_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    if request.user.role != 'admin':
        return api.create_response(request, {"error": "Forbidden"}, status=403)

    leave = get_object_or_404(LeaveRequest.objects.select_related('user'), id=leave_id)
    leave.status = 'approved'
    leave.save()
    _notify(
        [leave.user],
        title='Leave Request Approved',
        message=f'Your {leave.get_leave_type_display()} request ({leave.start_date} – {leave.end_date}) has been approved.',
        notif_type='leave_approved',
    )
    return _build_response(leave)


@api.put("/leave-requests/{leave_id}/reject", response=LeaveResponse)
def reject_leave_request(request, leave_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {"error": "Not authenticated"}, status=401)
    if request.user.role != 'admin':
        return api.create_response(request, {"error": "Forbidden"}, status=403)

    leave = get_object_or_404(LeaveRequest.objects.select_related('user'), id=leave_id)
    leave.status = 'rejected'
    leave.save()
    _notify(
        [leave.user],
        title='Leave Request Rejected',
        message=f'Your {leave.get_leave_type_display()} request ({leave.start_date} – {leave.end_date}) has been rejected.',
        notif_type='leave_rejected',
    )
    return _build_response(leave)


@api.get("/leave-types", response=LeaveTypesResponse)
def get_leave_types(request):
    """Get all available leave types for the application form."""
    leave_types = [
        ChoiceItem(value=value, label=label)
        for value, label in LeaveRequest.LEAVE_TYPE_CHOICES
    ]
    return LeaveTypesResponse(leave_types=leave_types)
