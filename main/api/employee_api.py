from ninja import File, Schema
from datetime import datetime, time
from typing import Optional
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models import Q
import base64
import os
from . import api
from main.models import User, EmployeeProfile, Address, BankDetails
from main.utils.email_utils import send_credentials_email
from .schemas import (
    AddressSchema, BankDetailsSchema,
    EmployeeCreateSchema, EmployeeUpdateSchema, EmployeeResponse, EmployeeListResponse
)


# Employee endpoints - for creating employees only (role is always "employee")
@api.get("/employees", response=EmployeeListResponse)
def list_employees(
    request,
    search: Optional[str] = None,
    department: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """List all employees with optional search, department filter, and pagination"""
    qs = User.objects.filter(role='employee').select_related('profile', 'address', 'bank')

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(profile__employee_id__icontains=search)
        )

    if department and department != 'All':
        qs = qs.filter(profile__department=department)

    total = qs.count()
    page_size = max(1, min(page_size, 100))
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size

    result = []
    for user in qs[offset:offset + page_size]:
        profile = getattr(user, 'profile', None)
        address = getattr(user, 'address', None)
        bank = getattr(user, 'bank', None)

        result.append(EmployeeResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            login_email=user.login_email,
            role=user.role,
            status=user.status,
            employee_id=profile.employee_id if profile else '',
            department=profile.department if profile else 'development',
            designation=profile.designation if profile else 'software_engineer',
            phone=profile.phone if profile else None,
            date_of_birth=str(profile.date_of_birth) if profile and profile.date_of_birth else None,
            gender=profile.gender if profile else None,
            fathers_name=profile.fathers_name if profile else None,
            marital_status=profile.marital_status if profile else None,
            blood_group=profile.blood_group if profile else None,
            religion=profile.religion if profile else None,
            check_in_time=str(profile.check_in_time) if profile and profile.check_in_time else None,
            check_out_time=str(profile.check_out_time) if profile and profile.check_out_time else None,
            date_of_leaving=str(profile.date_of_leaving) if profile and profile.date_of_leaving else None,
            avatar_url=get_avatar_url(user),
            join_date=profile.join_date if profile else user.created_at,
            created_at=user.created_at,
            address=AddressSchema(
                street=address.street,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country
            ) if address else None,
            bank=BankDetailsSchema(
                account_number=bank.account_number,
                bank_name=bank.bank_name,
                ifsc_code=bank.ifsc_code
            ) if bank else None
        ))

    return {
        'employees': result,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
    }


def generate_employee_id():
    """Generate sequential employee ID like AUC001, AUC002"""
    import re
    profiles = EmployeeProfile.objects.all()
    max_num = 0

    for profile in profiles:
        emp_id = profile.employee_id
        if emp_id:
            match = re.search(r'AUC(\d+)', emp_id.upper())
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

    next_num = max_num + 1
    return f"AUC{next_num:03d}"


def save_base64_avatar(user: User, base64_data: str):
    """Convert base64 image data to Django ImageField file"""
    if not base64_data:
        return
    
    try:
        # Parse base64 data (format: data:image/png;base64,xxxxx or just xxxxx)
        if ',' in base64_data:
            format_info, img_data = base64_data.split(',', 1)
            # Extract extension from format info
            if 'image/' in format_info:
                ext = format_info.split('image/')[1].split(';')[0]
            else:
                ext = 'png'
        else:
            img_data = base64_data
            ext = 'png'
        
        # Decode base64
        image_bytes = base64.b64decode(img_data)
        
        # Create filename
        filename = f"avatar_{user.id}.{ext}"
        
        # Save to ImageField
        user.avatar.save(filename, ContentFile(image_bytes), save=True)
    except Exception as e:
        print(f"Error saving avatar: {e}")


def get_avatar_url(user: User) -> Optional[str]:
    """Get the avatar URL for a user"""
    if user.avatar and user.avatar.name:
        return f"/media/{user.avatar.name}"
    return None


@api.post("/employees", response=EmployeeResponse)
def create_employee(request, payload: EmployeeCreateSchema):
    """Create a new employee with profile, address and bank details"""
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

    # Check if phone already exists
    if payload.phone and EmployeeProfile.objects.filter(phone=payload.phone).exists():
        return api.create_response(
            request,
            {"error": "Phone number already in use. Please use a different number."},
            status=400
        )

    # Auto-generate employee_id if not provided
    employee_id = payload.employee_id or generate_employee_id()
    
    # Create user with role='employee'
    user = User.objects.create_user(
        email=payload.email,
        login_email=payload.login_email,
        password=payload.password,
        name=payload.name.title(),
        role='employee'
    )
    send_credentials_email(
        name=payload.name.title(),
        email=payload.email,
        login_email=payload.login_email,
        password=payload.password,
        role='employee',
    )

    # Save avatar if provided (base64)
    if payload.avatar_base64:
        save_base64_avatar(user, payload.avatar_base64)
    
    # Create employee profile with all personal info
    profile = EmployeeProfile.objects.create(
        user=user,
        employee_id=employee_id,
        department=payload.department,
        designation=payload.designation,
        phone=payload.phone,
        date_of_birth=payload.date_of_birth if payload.date_of_birth else None,
        gender=payload.gender,
        fathers_name=payload.fathers_name,
        marital_status=payload.marital_status,
        blood_group=payload.blood_group,
        religion=payload.religion,
        check_in_time=time.fromisoformat(payload.check_in_time) if payload.check_in_time else None,
        check_out_time=time.fromisoformat(payload.check_out_time) if payload.check_out_time else None
    )
    
    # Create address if provided
    address_obj = None
    if payload.address:
        address_obj = Address.objects.create(
            user=user,
            street=payload.address.street or '',
            city=payload.address.city or '',
            state=payload.address.state or '',
            zip_code=payload.address.zip_code or '',
            country=payload.address.country or ''
        )
    
    # Create bank details if provided
    bank_obj = None
    if payload.bank:
        bank_obj = BankDetails.objects.create(
            user=user,
            account_number=payload.bank.account_number or '',
            bank_name=payload.bank.bank_name or '',
            ifsc_code=payload.bank.ifsc_code or ''
        )
    
    return _build_employee_response(user, profile, address_obj, bank_obj)


def _build_employee_response(user: User, profile: EmployeeProfile, address: Address = None, bank: BankDetails = None) -> EmployeeResponse:
    """Helper function to build EmployeeResponse from models"""
    return EmployeeResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        login_email=user.login_email,
        role=user.role,
        status=user.status,
        employee_id=profile.employee_id if profile else '',
        department=profile.department if profile else 'development',
        designation=profile.designation if profile else 'software_engineer',
        phone=profile.phone if profile else None,
        date_of_birth=str(profile.date_of_birth) if profile and profile.date_of_birth else None,
        gender=profile.gender if profile else None,
        fathers_name=profile.fathers_name if profile else None,
        marital_status=profile.marital_status if profile else None,
        blood_group=profile.blood_group if profile else None,
        religion=profile.religion if profile else None,
        check_in_time=str(profile.check_in_time) if profile and profile.check_in_time else None,
        check_out_time=str(profile.check_out_time) if profile and profile.check_out_time else None,
        date_of_leaving=str(profile.date_of_leaving) if profile and profile.date_of_leaving else None,
        avatar_url=get_avatar_url(user),  # Return avatar URL
        join_date=profile.join_date if profile else user.created_at,
        created_at=user.created_at,
        address=AddressSchema(
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country=address.country
        ) if address else None,
        bank=BankDetailsSchema(
            account_number=bank.account_number,
            bank_name=bank.bank_name,
            ifsc_code=bank.ifsc_code
        ) if bank else None
    )


@api.get("/employees/{employee_id}", response=EmployeeResponse)
def get_employee(request, employee_id: int):
    """Get employee by ID"""
    user = User.objects.get(id=employee_id, role='employee')
    profile = getattr(user, 'profile', None)
    address = getattr(user, 'address', None)
    bank = getattr(user, 'bank', None)
    return _build_employee_response(user, profile, address, bank)


@api.put("/employees/{employee_id}", response=EmployeeResponse)
def update_employee(request, employee_id: int, payload: EmployeeUpdateSchema):
    """Update employee, profile, address and bank details"""
    user = User.objects.get(id=employee_id, role='employee')

    # Check if phone is taken by a different employee
    if payload.phone and EmployeeProfile.objects.filter(phone=payload.phone).exclude(user_id=employee_id).exists():
        return api.create_response(
            request,
            {"error": "Phone number already in use. Please use a different number."},
            status=400
        )

    user.name = payload.name.title()
    user.email = payload.email
    user.login_email = payload.login_email
    if payload.status:
        user.status = payload.status
    # Update avatar if new image provided (base64)
    if payload.avatar_base64:
        save_base64_avatar(user, payload.avatar_base64)
    user.save()
    
    # Update or create profile with all personal info
    profile, created = EmployeeProfile.objects.get_or_create(user=user)
    profile.employee_id = payload.employee_id
    profile.department = payload.department
    profile.designation = payload.designation
    profile.phone = payload.phone
    if payload.date_of_birth:
        profile.date_of_birth = payload.date_of_birth
    if payload.gender:
        profile.gender = payload.gender
    if payload.fathers_name:
        profile.fathers_name = payload.fathers_name
    if payload.marital_status:
        profile.marital_status = payload.marital_status
    if payload.blood_group:
        profile.blood_group = payload.blood_group
    if payload.religion:
        profile.religion = payload.religion
    if payload.check_in_time:
        profile.check_in_time = time.fromisoformat(payload.check_in_time)
    if payload.check_out_time:
        profile.check_out_time = time.fromisoformat(payload.check_out_time)
    profile.date_of_leaving = payload.date_of_leaving if payload.date_of_leaving else None
    profile.save()
    
    # Update or create address
    address_obj = getattr(user, 'address', None)
    if payload.address:
        if not address_obj:
            address_obj, _ = Address.objects.get_or_create(user=user)
        address_obj.street = payload.address.street or address_obj.street
        address_obj.city = payload.address.city or address_obj.city
        address_obj.state = payload.address.state or address_obj.state
        address_obj.zip_code = payload.address.zip_code or address_obj.zip_code
        address_obj.country = payload.address.country or address_obj.country
        address_obj.save()
    
    # Update or create bank details
    bank_obj = getattr(user, 'bank', None)
    if payload.bank:
        if not bank_obj:
            bank_obj, _ = BankDetails.objects.get_or_create(user=user)
        bank_obj.account_number = payload.bank.account_number or bank_obj.account_number
        bank_obj.bank_name = payload.bank.bank_name or bank_obj.bank_name
        bank_obj.ifsc_code = payload.bank.ifsc_code or bank_obj.ifsc_code
        bank_obj.save()
    
    return _build_employee_response(user, profile, address_obj, bank_obj)


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    """Delete employee (user with role='employee')"""
    user = User.objects.get(id=employee_id, role='employee')
    user.delete()
    return {"success": True, "message": "Employee deleted successfully"}
