from ninja import Schema
from datetime import date, datetime
from typing import Optional, List


class LeadSchema(Schema):
    id: int
    client_name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    lead_from: Optional[str] = None
    lead_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class LeadCreateSchema(Schema):
    client_name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    lead_from: Optional[str] = None
    lead_date: Optional[date] = None


class LeadUpdateSchema(Schema):
    client_name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    lead_from: Optional[str] = None
    lead_date: Optional[date] = None


class LeadListResponse(Schema):
    leads: List[LeadSchema]
    total: int
    page: int
    page_size: int
    total_pages: int
