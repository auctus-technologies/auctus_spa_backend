# Schemas package
from .attendance_schemas import (
    AttendanceCreateSchema, AttendanceUpdateSchema, AttendanceResponse, AttendanceStatsSchema,
    MarkFaceAttendanceSchema, MarkFaceAttendanceResponse, FaceAttendanceErrorResponse,
)
from .common_schemas import AddressSchema, BankDetailsSchema
from .core_schemas import (
    HealthResponse, DashboardStats,
    ProjectSchema, ProjectCreateSchema
)
from .lead_schemas import (
    LeadSchema, LeadCreateSchema, LeadUpdateSchema, LeadListResponse,
)
from .client_schemas import (
    ClientSchema, ClientCreateSchema, ClientUpdateSchema, ClientListResponse
)
from .employee_schemas import EmployeeCreateSchema, EmployeeUpdateSchema, EmployeeResponse, EmployeeListResponse
from .opening_schemas import (
    OpeningCreateSchema, OpeningUpdateSchema, OpeningResponse, OpeningListResponse,
    FormChoicesResponse, ChoiceItem,
)
from .user_schemas import (
    UserSchema, UserMeSchema, UserCreateSchema, UserUpdateSchema, UserResponse, UserListResponse,
    LoginRequest, LoginResponse, ChangePasswordRequest, ChangePasswordResponse
)
from .leave_schemas import LeaveResponse, LeaveDocumentSchema, ChoiceItem, LeaveTypesResponse
from .holiday_schemas import HolidaySchema, HolidayCreateSchema, HolidayUpdateSchema, HolidayListResponse
from .salary_schemas import SalaryCreateSchema, SalaryUpdateSchema, SalaryResponse, SalaryListResponse

__all__ = [
    'AttendanceCreateSchema', 'AttendanceUpdateSchema', 'AttendanceResponse', 'AttendanceStatsSchema',
    'MarkFaceAttendanceSchema', 'MarkFaceAttendanceResponse', 'FaceAttendanceErrorResponse',
    'AddressSchema', 'BankDetailsSchema',
    'HealthResponse', 'DashboardStats',
    'LeadSchema', 'LeadCreateSchema', 'LeadUpdateSchema', 'LeadListResponse',
    'ClientSchema', 'ClientCreateSchema', 'ClientUpdateSchema', 'ClientListResponse',
    'ProjectSchema', 'ProjectCreateSchema',
    'EmployeeCreateSchema', 'EmployeeUpdateSchema', 'EmployeeResponse', 'EmployeeListResponse',
    'OpeningCreateSchema', 'OpeningUpdateSchema', 'OpeningResponse', 'OpeningListResponse',
    'FormChoicesResponse', 'ChoiceItem',
    'UserSchema', 'UserMeSchema', 'UserCreateSchema', 'UserUpdateSchema', 'UserResponse', 'UserListResponse',
    'LoginRequest', 'LoginResponse', 'ChangePasswordRequest', 'ChangePasswordResponse',
    'LeaveResponse', 'LeaveDocumentSchema', 'ChoiceItem', 'LeaveTypesResponse',
    'HolidaySchema', 'HolidayCreateSchema', 'HolidayUpdateSchema', 'HolidayListResponse',
    'SalaryCreateSchema', 'SalaryUpdateSchema', 'SalaryResponse', 'SalaryListResponse',
]
