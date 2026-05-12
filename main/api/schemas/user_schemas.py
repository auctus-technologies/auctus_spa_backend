from ninja import Schema
from typing import Optional, List


class UserSchema(Schema):
    id: int
    name: str
    username: str
    email: str
    role: str | None = None


class UserMeSchema(Schema):
    id: int
    name: str
    email: str
    login_email: str
    role: str
    status: str
    designation: Optional[str] = None
    department: Optional[str] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None


class UserCreateSchema(Schema):
    name: str
    email: str
    login_email: str
    password: str
    role: str = "employee"


class UserUpdateSchema(Schema):
    name: str
    email: str
    login_email: str
    role: str  # No default - must be explicitly provided


class UserResponse(Schema):
    id: int
    name: str
    email: str
    login_email: str
    role: str
    status: str


class UserListResponse(Schema):
    users: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Authentication Schemas
class LoginRequest(Schema):
    login_email: str
    password: str


class LoginResponse(Schema):
    success: bool
    message: str
    user: UserSchema | None = None

class ChangePasswordRequest(Schema):
    current_password: str | None = None
    new_password: str


class ChangePasswordResponse(Schema):
    success: bool
    message: str
