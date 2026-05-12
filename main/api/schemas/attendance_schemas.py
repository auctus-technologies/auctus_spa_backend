from ninja import Schema
from datetime import date
from typing import Optional


class AttendanceCreateSchema(Schema):
    user_id: int
    date: date
    check_in_time: Optional[str] = None  # ISO format time string
    check_out_time: Optional[str] = None  # ISO format time string


class AttendanceUpdateSchema(Schema):
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    status: Optional[str] = None


class AttendanceResponse(Schema):
    id: int
    user_id: int
    user_name: str
    date: date
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    status: str


class AttendanceStatsSchema(Schema):
    total_employees: int
    present_today: int
    leave_today: int
    late_checkins: int


class MarkFaceAttendanceSchema(Schema):
    phone: str
    photo_base64: str
    address: Optional[str] = None


class MarkFaceAttendanceResponse(Schema):
    success: bool
    action: str  # "check_in" or "check_out"
    user_name: str
    employee_id: str
    designation: str
    department: str
    match_confidence: float
    is_late: bool = False
    check_in_time: Optional[str] = None
    check_in_date: Optional[str] = None
    check_in_address: Optional[str] = None
    check_out_time: Optional[str] = None
    check_out_date: Optional[str] = None
    check_out_address: Optional[str] = None


class FaceAttendanceErrorResponse(Schema):
    error: str
    message: str
