from ninja import Schema
from datetime import date, datetime
from typing import List, Optional


class HolidaySchema(Schema):
    id: int
    name: str
    date: date
    created_at: datetime


class HolidayCreateSchema(Schema):
    name: str
    date: date


class HolidayUpdateSchema(Schema):
    name: Optional[str] = None
    date: Optional[date] = None


class HolidayListResponse(Schema):
    holidays: List[HolidaySchema]
    total: int
