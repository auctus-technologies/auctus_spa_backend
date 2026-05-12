from typing import Optional
from django.db.models import Q
from django.shortcuts import get_object_or_404
from . import api
from main.models import Salary, User
from main.models.employee_profile import EmployeeProfile
from .schemas import SalaryCreateSchema, SalaryUpdateSchema, SalaryResponse, SalaryListResponse


def _build_response(s: Salary) -> SalaryResponse:
    profile = getattr(s.user, 'profile', None)
    dept_key  = profile.department  if profile else ''
    desig_key = profile.designation if profile else ''
    dept_label  = dict(EmployeeProfile.DEPARTMENT_CHOICES).get(dept_key, dept_key)
    desig_label = dict(EmployeeProfile.DESIGNATION_CHOICES).get(desig_key, desig_key)
    return SalaryResponse(
        id=s.id,
        user_id=s.user_id,
        user_name=s.user.name,
        employee_id=profile.employee_id if profile else '',
        designation=desig_key,
        designation_label=desig_label,
        department=dept_key,
        department_label=dept_label,
        basic=float(s.basic),
        hra=float(s.hra),
        da=float(s.da),
        travel_allowance=float(s.travel_allowance),
        medical_allowance=float(s.medical_allowance),
        other_allowance=float(s.other_allowance),
        pf=float(s.pf),
        esi=float(s.esi),
        professional_tax=float(s.professional_tax),
        tds=float(s.tds),
        other_deduction=float(s.other_deduction),
        effective_date=s.effective_date,
    )


@api.get("/salary", response=SalaryListResponse)
def list_salary(
    request,
    search: Optional[str] = None,
    department: Optional[str] = None,
    user_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 10,
):
    qs = Salary.objects.select_related('user', 'user__profile')

    if user_id:
        qs = qs.filter(user_id=user_id)
    if search:
        qs = qs.filter(
            Q(user__name__icontains=search) |
            Q(user__profile__employee_id__icontains=search)
        )
    if department and department != 'All':
        qs = qs.filter(user__profile__department=department)

    total = qs.count()
    page_size  = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return SalaryListResponse(
        salaries=[_build_response(s) for s in qs[offset:offset + page_size]],
        total=total,
        total_pages=total_pages,
    )


@api.post("/salary", response=SalaryResponse)
def create_salary(request, payload: SalaryCreateSchema):
    user = get_object_or_404(User, id=payload.user_id)
    if hasattr(user, 'salary'):
        # Already has a record — return existing (frontend should use PUT to update)
        return _build_response(user.salary)
    s = Salary.objects.create(
        user=user,
        basic=payload.basic,
        hra=payload.hra,
        da=payload.da,
        travel_allowance=payload.travel_allowance,
        medical_allowance=payload.medical_allowance,
        other_allowance=payload.other_allowance,
        pf=payload.pf,
        esi=payload.esi,
        professional_tax=payload.professional_tax,
        tds=payload.tds,
        other_deduction=payload.other_deduction,
    )
    return _build_response(s)


@api.put("/salary/{salary_id}", response=SalaryResponse)
def update_salary(request, salary_id: int, payload: SalaryUpdateSchema):
    s = get_object_or_404(Salary.objects.select_related('user', 'user__profile'), id=salary_id)
    fields = [
        'basic', 'hra', 'da', 'travel_allowance', 'medical_allowance',
        'other_allowance', 'pf', 'esi', 'professional_tax', 'tds',
        'other_deduction', 'effective_date',
    ]
    for f in fields:
        v = getattr(payload, f)
        if v is not None:
            setattr(s, f, v)
    s.save()
    return _build_response(s)


@api.delete("/salary/{salary_id}")
def delete_salary(request, salary_id: int):
    s = get_object_or_404(Salary, id=salary_id)
    s.delete()
    return {"success": True}
