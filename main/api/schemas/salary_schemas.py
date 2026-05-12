from ninja import Schema
from typing import Optional, List
from datetime import date


class SalaryCreateSchema(Schema):
    user_id: int
    basic: float = 0
    hra: float = 0
    da: float = 0
    travel_allowance: float = 0
    medical_allowance: float = 0
    other_allowance: float = 0
    pf: float = 0
    esi: float = 0
    professional_tax: float = 0
    tds: float = 0
    other_deduction: float = 0


class SalaryUpdateSchema(Schema):
    basic: Optional[float] = None
    hra: Optional[float] = None
    da: Optional[float] = None
    travel_allowance: Optional[float] = None
    medical_allowance: Optional[float] = None
    other_allowance: Optional[float] = None
    pf: Optional[float] = None
    esi: Optional[float] = None
    professional_tax: Optional[float] = None
    tds: Optional[float] = None
    other_deduction: Optional[float] = None
    effective_date: Optional[date] = None


class SalaryResponse(Schema):
    id: int
    user_id: int
    user_name: str
    employee_id: str
    designation: str
    designation_label: str
    department: str
    department_label: str
    basic: float
    hra: float
    da: float
    travel_allowance: float
    medical_allowance: float
    other_allowance: float
    pf: float
    esi: float
    professional_tax: float
    tds: float
    other_deduction: float
    effective_date: Optional[date] = None


class SalaryListResponse(Schema):
    salaries: List[SalaryResponse]
    total: int
    total_pages: int
