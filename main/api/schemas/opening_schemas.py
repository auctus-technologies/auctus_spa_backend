from ninja import Schema
from typing import Optional, List
from datetime import datetime


class OpeningCreateSchema(Schema):
    job_title: str
    department: Optional[str] = None
    role: Optional[str] = None
    qualification_required: Optional[str] = None
    required_experience: Optional[int] = None
    responsibilities: Optional[str] = None
    skills_required: Optional[str] = None
    location: Optional[str] = None


class OpeningUpdateSchema(Schema):
    job_title: str
    department: Optional[str] = None
    role: Optional[str] = None
    qualification_required: Optional[str] = None
    required_experience: Optional[int] = None
    responsibilities: Optional[str] = None
    skills_required: Optional[str] = None
    location: Optional[str] = None
    status: str = 'active'


class OpeningResponse(Schema):
    id: int
    job_title: str
    department: Optional[str] = None
    role: Optional[str] = None
    qualification_required: Optional[str] = None
    required_experience: Optional[int] = None
    responsibilities: Optional[str] = None
    skills_required: Optional[str] = None
    location: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class OpeningListResponse(Schema):
    openings: List[OpeningResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ChoiceItem(Schema):
    value: str
    label: str


class FormChoicesResponse(Schema):
    departments: List[ChoiceItem]
    designations: List[ChoiceItem]
