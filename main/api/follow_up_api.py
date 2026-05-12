from typing import List
from django.shortcuts import get_object_or_404
from . import api
from main.models import Lead, User, EmployeeProfile
from main.models.lead_follow_up import LeadFollowUp
from .schemas.follow_up_schemas import (
    LeadFollowUpSchema, LeadFollowUpCreateSchema, LeadFollowUpUpdateSchema,
    FollowUpUserSchema,
)


def _to_schema(fu: LeadFollowUp) -> LeadFollowUpSchema:
    return LeadFollowUpSchema(
        id=fu.id,
        lead_id=fu.lead_id,
        follow_up_user_id=fu.follow_up_user_id,
        follow_up_user_name=fu.follow_up_user.name if fu.follow_up_user else None,
        follow_up_date=fu.follow_up_date,
        notes=fu.notes,
        created_at=fu.created_at,
        updated_at=fu.updated_at,
    )


@api.get('/lead-follow-up-users', response=List[FollowUpUserSchema])
def get_follow_up_users(request):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    profiles = EmployeeProfile.objects.filter(
        department__in=['marketing', 'sales'],
        user__status__iexact='active',
    ).select_related('user').order_by('user__name')

    return [
        FollowUpUserSchema(
            id=p.user.id,
            name=p.user.name,
            designation=p.designation,
            department=p.department,
        )
        for p in profiles
    ]


@api.get('/leads/{lead_id}/follow-ups', response=List[LeadFollowUpSchema])
def list_follow_ups(request, lead_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    lead = get_object_or_404(Lead, id=lead_id)
    return [_to_schema(fu) for fu in lead.follow_ups.select_related('follow_up_user').all()]


@api.post('/leads/{lead_id}/follow-ups', response=LeadFollowUpSchema)
def create_follow_up(request, lead_id: int, data: LeadFollowUpCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    lead = get_object_or_404(Lead, id=lead_id)

    follow_up_user = None
    if data.follow_up_user_id:
        try:
            follow_up_user = User.objects.get(id=data.follow_up_user_id)
        except User.DoesNotExist:
            pass

    fu = LeadFollowUp.objects.create(
        lead=lead,
        follow_up_user=follow_up_user,
        follow_up_date=data.follow_up_date,
        notes=data.notes or None,
    )
    fu.refresh_from_db()
    return _to_schema(fu)


@api.put('/leads/{lead_id}/follow-ups/{follow_up_id}', response=LeadFollowUpSchema)
def update_follow_up(request, lead_id: int, follow_up_id: int, data: LeadFollowUpUpdateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    fu = get_object_or_404(LeadFollowUp, id=follow_up_id, lead_id=lead_id)

    if data.follow_up_user_id:
        try:
            fu.follow_up_user = User.objects.get(id=data.follow_up_user_id)
        except User.DoesNotExist:
            fu.follow_up_user = None
    else:
        fu.follow_up_user = None

    fu.follow_up_date = data.follow_up_date
    fu.notes = data.notes or None
    fu.save()
    fu.refresh_from_db()
    return _to_schema(fu)


@api.delete('/leads/{lead_id}/follow-ups/{follow_up_id}')
def delete_follow_up(request, lead_id: int, follow_up_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    fu = get_object_or_404(LeadFollowUp, id=follow_up_id, lead_id=lead_id)
    fu.delete()
    return {'success': True}
