from ninja import Schema
from typing import Optional, List
from datetime import datetime


class ApplicationCreateSchema(Schema):
    opening_id:  Optional[int] = None
    full_name:   str
    email:       str
    phone:       Optional[str] = None
    city:        Optional[str] = None
    experience:  Optional[int] = None


class ApplicationStatusUpdateSchema(Schema):
    status: str


class ApplicationResponse(Schema):
    id:           int
    opening_id:   Optional[int] = None
    opening_title: Optional[str] = None
    full_name:    str
    email:        str
    phone:        Optional[str] = None
    city:         Optional[str] = None
    experience:   Optional[int] = None
    resume:       Optional[str] = None
    status:       str
    applied_at:   datetime
    updated_at:   datetime


class ApplicationListResponse(Schema):
    applications: List[ApplicationResponse]
    total:        int
    page:         int
    page_size:    int
    total_pages:  int
