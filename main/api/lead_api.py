from typing import Optional, List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from . import api
from main.models import Lead, Client
from .schemas.lead_schemas import (
    LeadSchema, LeadCreateSchema, LeadUpdateSchema, LeadListResponse,
)


def _to_schema(lead: Lead) -> LeadSchema:
    return LeadSchema(
        id=lead.id,
        client_name=lead.client_name,
        company_name=lead.company_name,
        email=lead.email,
        phone=lead.phone,
        address=lead.address,
        country=lead.country,
        state=lead.state,
        status=lead.status,
        lead_from=lead.lead_from,
        lead_date=lead.lead_date,
        created_at=lead.created_at,
        updated_at=lead.updated_at,
    )



@api.get('/leads', response=LeadListResponse)
def list_leads(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    lead_from: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    qs = Lead.objects.all()

    if search:
        qs = qs.filter(
            Q(client_name__icontains=search) |
            Q(company_name__icontains=search) |
            Q(email__icontains=search)
        )
    if status and status != 'All':
        qs = qs.filter(status=status)
    if lead_from and lead_from != 'All':
        qs = qs.filter(lead_from=lead_from)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return LeadListResponse(
        leads=[_to_schema(l) for l in qs[offset:offset + page_size]],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@api.post('/leads', response=LeadSchema)
def create_lead(request, data: LeadCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    lead = Lead.objects.create(
        client_name=data.client_name,
        company_name=data.company_name or None,
        email=data.email or None,
        phone=data.phone or None,
        address=data.address or None,
        country=data.country or None,
        state=data.state or None,
        status=data.status or None,
        lead_from=data.lead_from or None,
        lead_date=data.lead_date,
    )
    return _to_schema(lead)


@api.get('/leads/{lead_id}', response=LeadSchema)
def get_lead(request, lead_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    lead = get_object_or_404(Lead, id=lead_id)
    return _to_schema(lead)


@api.put('/leads/{lead_id}', response=LeadSchema)
def update_lead(request, lead_id: int, data: LeadUpdateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    lead = get_object_or_404(Lead, id=lead_id)

    lead.client_name = data.client_name
    lead.company_name = data.company_name or None
    lead.email = data.email or None
    lead.phone = data.phone or None
    lead.address = data.address or None
    lead.country = data.country or None
    lead.state = data.state or None
    lead.status = data.status or None
    lead.lead_from = data.lead_from or None
    lead.lead_date = data.lead_date
    lead.save()
    return _to_schema(lead)


@api.delete('/leads/{lead_id}')
def delete_lead(request, lead_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return {'success': True}


@api.post('/leads/{lead_id}/convert-to-client', response=LeadSchema)
def convert_lead_to_client(request, lead_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {'error': 'Not authenticated'}, status=401)

    lead = get_object_or_404(Lead, id=lead_id)

    if lead.status == 'client':
        return api.create_response(request, {'error': 'Lead is already a client'}, status=400)

    # Create client from lead data (skip if email already exists)
    if lead.email and Client.objects.filter(email=lead.email).exists():
        pass  # client already exists, just update lead status
    else:
        client_kwargs = {
            'name': lead.client_name,
            'phone': lead.phone,
            'company': lead.company_name,
            'address': lead.address,
            'country': lead.country,
            'state': lead.state,
        }
        if lead.email:
            client_kwargs['email'] = lead.email
            Client.objects.create(**client_kwargs)
        else:
            Client.objects.create(email='', **client_kwargs)

    lead.status = 'client'
    lead.save()
    return _to_schema(lead)
