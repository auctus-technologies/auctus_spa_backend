from datetime import datetime
from typing import Optional
from django.db.models import Q
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from . import api
from main.models import User
from main.utils.email_utils import send_credentials_email
from .schemas import (
    UserSchema, UserMeSchema, UserCreateSchema, UserUpdateSchema, UserResponse, UserListResponse,
    LoginRequest, LoginResponse, ChangePasswordRequest, ChangePasswordResponse
)


# Users endpoints
@api.get("/users", response=list[UserResponse])
def list_users(request):
    users = User.objects.all()
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            login_email=user.login_email,
            role=user.role,
            status=user.status,
        )
        for user in users
    ]


@api.get("/admins", response=UserListResponse)
def list_admins(
    request,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """List admin users with optional search and pagination"""
    qs = User.objects.filter(role='admin')

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(login_email__icontains=search)
        )

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    return {
        'users': [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                login_email=user.login_email,
                role=user.role,
                status=user.status,
            )
            for user in qs[offset:offset + page_size]
        ],
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
    }


@api.post("/users", response=UserResponse)
def create_user(request, payload: UserCreateSchema):
    # Check if login_email already exists
    if User.objects.filter(login_email=payload.login_email).exists():
        return api.create_response(
            request,
            {"error": "Login email already exists"},
            status=400
        )
    
    # Check if email already exists
    if User.objects.filter(email=payload.email).exists():
        return api.create_response(
            request,
            {"error": "Email already exists"},
            status=400
        )
    
    user = User.objects.create_user(
        email=payload.email,
        login_email=payload.login_email,
        password=payload.password,
        name=payload.name,
        role=payload.role
    )
    send_credentials_email(
        name=payload.name,
        email=payload.email,
        login_email=payload.login_email,
        password=payload.password,
        role=payload.role,
    )
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        login_email=user.login_email,
        role=user.role,
        status=user.status,
        created_at=user.created_at
    )


@api.get("/users/{user_id}", response=UserResponse)
def get_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        login_email=user.login_email,
        role=user.role,
        status=user.status,
        created_at=user.created_at
    )


@api.put("/users/{user_id}", response=UserResponse)
def update_user(request, user_id: int, payload: UserUpdateSchema):
    user = User.objects.get(id=user_id)
    user.name = payload.name
    user.email = payload.email
    user.login_email = payload.login_email
    user.role = payload.role
    user.save()
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        login_email=user.login_email,
        role=user.role,
        status=user.status,
        created_at=user.created_at
    )


@api.delete("/users/{user_id}")
def delete_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    user.delete()
    return {"success": True, "message": "User deleted successfully"}


# Authentication endpoints
@api.post("/auth/login", response=LoginResponse)
def login(request, payload: LoginRequest):
    user = authenticate(
        request,
        username=payload.login_email,
        password=payload.password
    )
    
    if user:
        django_login(request, user)
        return LoginResponse(
            success=True,
            message="Login successful",
            user=UserSchema(
                id=user.id,
                name=user.name,
                username=user.login_email,
                email=user.email,
                first_name=user.name,
                last_name="",
                role=user.role
            )
        )
    else:
        return LoginResponse(
            success=False,
            message="Invalid credentials"
        )


@api.get("/auth/me", response=UserMeSchema)
def get_current_user(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        return UserMeSchema(
            id=request.user.id,
            name=request.user.name,
            email=request.user.email,
            login_email=request.user.login_email,
            role=request.user.role,
            status=request.user.status,
            designation=profile.designation if profile else None,
            department=profile.department if profile else None,
            check_in_time=str(profile.check_in_time) if profile and profile.check_in_time else None,
            check_out_time=str(profile.check_out_time) if profile and profile.check_out_time else None,
        )
    
    return UserMeSchema(
        id=0,
        name="Guest",
        email="",
        login_email="",
        role="guest",
        status="inactive"
    )


@api.post("/auth/logout")
def logout(request):
    django_logout(request)
    return {"success": True, "message": "Logged out successfully"}


@api.put("/users/{user_id}/change-password", response=ChangePasswordResponse)
def change_password(request, user_id: int, payload: ChangePasswordRequest):
    if not request.user.is_authenticated:
        return ChangePasswordResponse(success=False, message="Not authenticated")
    
    # Get the target user
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return ChangePasswordResponse(success=False, message="User not found")
    
    # Only check current password if user is changing their own password
    if request.user.id == user_id and hasattr(payload, 'current_password') and payload.current_password:
        if not request.user.check_password(payload.current_password):
            return ChangePasswordResponse(success=False, message="Current password is incorrect")
    
    target_user.set_password(payload.new_password)
    target_user.save()
    return ChangePasswordResponse(success=True, message="Password changed successfully")