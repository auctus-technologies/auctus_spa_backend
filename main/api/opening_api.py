from typing import Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q
from . import api
from main.models import JobOpening
from main.models.employee_profile import EmployeeProfile
from .schemas.opening_schemas import (
    OpeningCreateSchema,
    OpeningUpdateSchema,
    OpeningResponse,
    OpeningListResponse,
    FormChoicesResponse,
    ChoiceItem,
)


def _build_response(opening: JobOpening) -> OpeningResponse:
    return OpeningResponse(
        id=opening.id,
        job_title=opening.job_title,
        department=opening.department,
        role=opening.role,
        qualification_required=opening.qualification_required,
        required_experience=opening.required_experience,
        responsibilities=opening.responsibilities,
        skills_required=opening.skills_required,
        location=opening.location,
        status=opening.status,
        created_at=opening.created_at,
        updated_at=opening.updated_at,
    )


@api.get('/openings/form-choices', response=FormChoicesResponse)
def get_form_choices(request):
    departments = [
        ChoiceItem(value=value, label=label)
        for value, label in EmployeeProfile.DEPARTMENT_CHOICES
    ]
    designations = [
        ChoiceItem(value=value, label=label)
        for value, label in EmployeeProfile.DESIGNATION_CHOICES
    ]
    return FormChoicesResponse(departments=departments, designations=designations)


@api.get('/openings', response=OpeningListResponse)
def list_openings(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    qs = JobOpening.objects.all()

    if search:
        qs = qs.filter(
            Q(job_title__icontains=search) |
            Q(department__icontains=search) |
            Q(location__icontains=search) |
            Q(role__icontains=search)
        )

    if status and status != 'All':
        qs = qs.filter(status=status)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return OpeningListResponse(
        openings=[_build_response(o) for o in qs[offset:offset + page_size]],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@api.post('/openings', response=OpeningResponse)
def create_opening(request, payload: OpeningCreateSchema):
    opening = JobOpening.objects.create(
        job_title=payload.job_title,
        department=payload.department,
        role=payload.role,
        qualification_required=payload.qualification_required,
        required_experience=payload.required_experience,
        responsibilities=payload.responsibilities,
        skills_required=payload.skills_required,
        location=payload.location,
    )
    return _build_response(opening)


@api.get('/openings/{opening_id}', response=OpeningResponse)
def get_opening(request, opening_id: int):
    opening = get_object_or_404(JobOpening, id=opening_id)
    return _build_response(opening)


@api.put('/openings/{opening_id}', response=OpeningResponse)
def update_opening(request, opening_id: int, payload: OpeningUpdateSchema):
    opening = get_object_or_404(JobOpening, id=opening_id)
    opening.job_title = payload.job_title
    opening.department = payload.department
    opening.role = payload.role
    opening.qualification_required = payload.qualification_required
    opening.required_experience = payload.required_experience
    opening.responsibilities = payload.responsibilities
    opening.skills_required = payload.skills_required
    opening.location = payload.location
    opening.status = payload.status
    opening.save()
    return _build_response(opening)


@api.delete('/openings/{opening_id}')
def delete_opening(request, opening_id: int):
    opening = get_object_or_404(JobOpening, id=opening_id)
    opening.delete()
    return {'success': True, 'message': 'Job opening deleted successfully'}
