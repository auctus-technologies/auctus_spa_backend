from ninja import Schema
from datetime import date, datetime
from typing import Optional, List


class FollowUpUserSchema(Schema):
    id: int
    name: str
    designation: Optional[str] = None
    department: Optional[str] = None


class LeadFollowUpSchema(Schema):
    id: int
    lead_id: int
    follow_up_user_id: Optional[int] = None
    follow_up_user_name: Optional[str] = None
    follow_up_date: date
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class LeadFollowUpCreateSchema(Schema):
    follow_up_user_id: Optional[int] = None
    follow_up_date: date
    notes: Optional[str] = None


class LeadFollowUpUpdateSchema(Schema):
    follow_up_user_id: Optional[int] = None
    follow_up_date: date
    notes: Optional[str] = None
