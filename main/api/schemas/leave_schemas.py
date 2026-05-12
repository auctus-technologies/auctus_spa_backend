from ninja import Schema
from datetime import date, datetime
from typing import Optional, List


class LeaveDocumentSchema(Schema):
    id: int
    file_url: str
    uploaded_at: datetime


class LeaveResponse(Schema):
    id: int
    user_id: int
    user_name: str
    employee_id: Optional[str] = None
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str
    documents: List[LeaveDocumentSchema]
    applied_date: date


class ChoiceItem(Schema):
    value: str
    label: str


class LeaveTypesResponse(Schema):
    leave_types: List[ChoiceItem]
