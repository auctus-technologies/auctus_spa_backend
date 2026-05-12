from typing import Optional
from django.db.models import Q
from . import api
from main.models import Client
from .schemas import (
    ClientSchema, ClientCreateSchema, ClientUpdateSchema, ClientListResponse
)


@api.get("/clients", response=ClientListResponse)
def list_clients(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    all_clients = Client.objects.all()
    active_count = all_clients.filter(status='active').count()
    inactive_count = all_clients.filter(status='inactive').count()

    qs = all_clients
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(company__icontains=search)
        )
    if status and status != 'All':
        qs = qs.filter(status=status)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return ClientListResponse(
        clients=[
            ClientSchema(
                id=client.id,
                name=client.name,
                email=client.email,
                phone=client.phone,
                company=client.company,
                address=client.address,
                country=client.country,
                state=client.state,
                status=client.status,
                projects_count=client.projects_count,
                join_date=client.join_date,
                created_at=client.created_at,
                updated_at=client.updated_at
            )
            for client in qs[offset:offset + page_size]
        ],
        total=total,
        active_count=active_count,
        inactive_count=inactive_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@api.post("/clients", response=ClientSchema)
def create_client(request, payload: ClientCreateSchema):
    # Check if email already exists
    if Client.objects.filter(email=payload.email).exists():
        return api.create_response(
            request,
            {"error": "Email already exists"},
            status=400
        )
    
    client = Client.objects.create(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        company=payload.company,
        address=payload.address,
        country=payload.country,
        state=payload.state,
        join_date=payload.join_date
    )
    
    return ClientSchema(
        id=client.id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company=client.company,
        address=client.address,
        country=client.country,
        state=client.state,
        status=client.status,
        projects_count=client.projects_count,
        join_date=client.join_date,
        created_at=client.created_at,
        updated_at=client.updated_at
    )


@api.get("/clients/{client_id}", response=ClientSchema)
def get_client(request, client_id: int):
    try:
        client = Client.objects.get(id=client_id)
        return ClientSchema(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            company=client.company,
            address=client.address,
            status=client.status,
            projects_count=client.projects_count,
            join_date=client.join_date,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
    except Client.DoesNotExist:
        return api.create_response(
            request,
            {"error": "Client not found"},
            status=404
        )


@api.put("/clients/{client_id}", response=ClientSchema)
def update_client(request, client_id: int, payload: ClientUpdateSchema):
    try:
        client = Client.objects.get(id=client_id)
        
        # Check if email already exists (excluding current client)
        if Client.objects.filter(email=payload.email).exclude(id=client_id).exists():
            return api.create_response(
                request,
                {"error": "Email already exists"},
                status=400
            )
        
        # Update fields
        client.name = payload.name
        client.email = payload.email
        client.phone = payload.phone
        client.company = payload.company
        client.address = payload.address
        if payload.country is not None:
            client.country = payload.country
        if payload.state is not None:
            client.state = payload.state
        if payload.status is not None:
            client.status = payload.status
        if payload.projects_count is not None:
            client.projects_count = payload.projects_count
        if payload.join_date is not None:
            client.join_date = payload.join_date
        
        client.save()
        
        return ClientSchema(
            id=client.id,
            name=client.name,
            email=client.email,
            phone=client.phone,
            company=client.company,
            address=client.address,
            country=client.country,
            state=client.state,
            status=client.status,
            projects_count=client.projects_count,
            join_date=client.join_date,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
    except Client.DoesNotExist:
        return api.create_response(
            request,
            {"error": "Client not found"},
            status=404
        )


@api.delete("/clients/{client_id}")
def delete_client(request, client_id: int):
    try:
        client = Client.objects.get(id=client_id)
        client.delete()
        return {"success": True, "message": "Client deleted successfully"}
    except Client.DoesNotExist:
        return api.create_response(
            request,
            {"error": "Client not found"},
            status=404
        )
