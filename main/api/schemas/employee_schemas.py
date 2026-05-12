from ninja import Schema
from datetime import datetime
from typing import Optional, List
from .common_schemas import AddressSchema, BankDetailsSchema


class EmployeeCreateSchema(Schema):
    name: str
    email: str
    login_email: str
    password: str
    employee_id: Optional[str] = None  # Auto-generated if not provided
    department: str = "development"
    designation: str = "software_engineer"
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    fathers_name: Optional[str] = None
    marital_status: Optional[str] = None
    blood_group: Optional[str] = None
    religion: Optional[str] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    address: Optional[AddressSchema] = None
    bank: Optional[BankDetailsSchema] = None


class EmployeeUpdateSchema(Schema):
    name: str
    email: str
    login_email: str
    employee_id: str
    department: str
    designation: str
    status: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    fathers_name: Optional[str] = None
    marital_status: Optional[str] = None
    blood_group: Optional[str] = None
    religion: Optional[str] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    date_of_leaving: Optional[str] = None
    address: Optional[AddressSchema] = None
    bank: Optional[BankDetailsSchema] = None


class EmployeeResponse(Schema):
    id: int
    name: str
    email: str
    login_email: str
    role: str
    status: str
    employee_id: str
    department: str
    designation: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    fathers_name: Optional[str] = None
    marital_status: Optional[str] = None
    blood_group: Optional[str] = None
    religion: Optional[str] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    date_of_leaving: Optional[str] = None
    avatar_url: Optional[str] = None  # URL to the avatar image
    join_date: datetime
    created_at: datetime
    address: Optional[AddressSchema] = None
    bank: Optional[BankDetailsSchema] = None


class EmployeeListResponse(Schema):
    employees: List[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
