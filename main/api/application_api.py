from typing import Optional
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Form, File
from ninja.files import UploadedFile
from ninja.errors import HttpError
from . import api
from main.models import JobApplication, JobOpening
from .schemas.application_schemas import (
    ApplicationStatusUpdateSchema,
    ApplicationResponse,
    ApplicationListResponse,
)


def _build_response(app: JobApplication) -> ApplicationResponse:
    return ApplicationResponse(
        id=app.id,
        opening_id=app.opening_id,
        opening_title=app.opening.job_title if app.opening else None,
        full_name=app.full_name,
        email=app.email,
        phone=app.phone,
        city=app.city,
        experience=app.experience,
        resume=app.resume.url if app.resume else None,
        status=app.status,
        applied_at=app.applied_at,
        updated_at=app.updated_at,
    )


@api.post('/applications', response=ApplicationResponse, auth=None)
def create_application(
    request,
    full_name:  Form[str],
    email:      Form[str],
    opening_id: Form[Optional[int]] = None,
    phone:      Form[Optional[str]] = None,
    city:       Form[Optional[str]] = None,
    experience: Form[Optional[int]] = None,
    resume:     File[Optional[UploadedFile]] = None,
):
    opening = None
    if opening_id:
        opening = get_object_or_404(JobOpening, id=opening_id)
        six_months_ago = timezone.now() - timedelta(days=180)
        qs = JobApplication.objects.filter(opening_id=opening_id, applied_at__gte=six_months_ago)
        already_applied = qs.filter(email=email).exists()
        if not already_applied and phone:
            already_applied = qs.filter(phone=phone).exists()
        if already_applied:
            raise HttpError(409, "You've already applied for this job. Please wait 6 months before reapplying.")

    app = JobApplication.objects.create(
        opening=opening,
        full_name=full_name,
        email=email,
        phone=phone,
        city=city,
        experience=experience,
        resume=resume,
    )
    return _build_response(app)


@api.get('/applications', response=ApplicationListResponse)
def list_applications(
    request,
    opening_id: Optional[int] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    qs = JobApplication.objects.select_related('opening').all()

    if opening_id:
        qs = qs.filter(opening_id=opening_id)
    if status:
        qs = qs.filter(status=status)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return ApplicationListResponse(
        applications=[_build_response(a) for a in qs[offset:offset + page_size]],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@api.get('/applications/{app_id}', response=ApplicationResponse)
def get_application(request, app_id: int):
    app = get_object_or_404(JobApplication, id=app_id)
    return _build_response(app)


@api.patch('/applications/{app_id}/status', response=ApplicationResponse)
def update_status(request, app_id: int, payload: ApplicationStatusUpdateSchema):
    valid = {'pending', 'approved', 'rejected', 'on_hold'}
    if payload.status not in valid:
        return api.create_response(request, {'error': 'Invalid status'}, status=400)
    app = get_object_or_404(JobApplication, id=app_id)
    app.status = payload.status
    app.save()
    return _build_response(app)


@api.delete('/applications/{app_id}')
def delete_application(request, app_id: int):
    app = get_object_or_404(JobApplication, id=app_id)
    app.delete()
    return {'success': True}
