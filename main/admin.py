from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('login_email', 'email', 'name', 'role', 'status', 'is_active')
    list_filter = ('role', 'status', 'is_active', 'is_staff')
    search_fields = ('login_email', 'email', 'name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('login_email', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'avatar', 'avatar_embedding')}),
        ('Permissions', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login_email', 'email', 'name', 'password1', 'password2', 'role'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'designation', 'join_date')
    list_filter = ('department', 'join_date')
    search_fields = ('employee_id', 'user__name', 'department', 'designation')


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'account_number', 'ifsc_code')
    search_fields = ('user__name', 'bank_name', 'account_number')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in_time', 'check_out_time')
    list_filter = ('date',)
    search_fields = ('user__name',)
    date_hierarchy = 'date'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country', 'zip_code')
    search_fields = ('user__name', 'city', 'state', 'country')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'country', 'state', 'status', 'projects_count')
    list_filter = ('status', 'country', 'state')
    search_fields = ('name', 'email', 'phone', 'company', 'country', 'state')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'client__name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProjectAttachment)
class ProjectAttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'project', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('file_name', 'project__name')
    readonly_fields = ('uploaded_at',)

class LeaveDocumentInline(admin.TabularInline):
    model = LeaveDocument
    extra = 1


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    search_fields = ('user__name', 'leave_type', 'reason')
    readonly_fields = ('created_at', 'updated_at', 'applied_date')
    inlines = [LeaveDocumentInline]


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'role', 'location', 'required_experience', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('job_title', 'location', 'role')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'opening', 'experience', 'city', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('full_name', 'email', 'phone', 'opening__job_title')
    readonly_fields = ('applied_at', 'updated_at')
    list_editable = ('status',)

