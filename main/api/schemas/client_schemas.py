from ninja import Schema
from typing import Optional
from datetime import datetime, date


class ClientSchema(Schema):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    status: str
    projects_count: int
    join_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class ClientCreateSchema(Schema):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    country: str
    state: Optional[str] = None
    join_date: Optional[date] = None


class ClientUpdateSchema(Schema):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    projects_count: Optional[int] = None
    join_date: Optional[date] = None


class ClientListResponse(Schema):
    clients: list[ClientSchema]
    total: int
    active_count: int
    inactive_count: int
    page: int = 1
    page_size: int = 10
    total_pages: int = 1
