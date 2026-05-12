from django.db import models
from .user import User


class EmployeeProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('management', 'Management'),
        ('development', 'Development'),
        ('hr', 'Human Resources (HR)'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
    ]

    DESIGNATION_CHOICES = [
        # Management
        ('manager', 'Manager'),
        ('assistant_manager', 'Assistant Manager'),
        # Development
        ('software_engineer', 'Software Engineer'),
        ('senior_developer', 'Senior Developer'),
        ('junior_developer', 'Junior Developer'),
        ('team_lead', 'Team Lead'),
        ('qa_engineer', 'QA Engineer'),
        ('devops_engineer', 'DevOps Engineer'),
        # HR
        ('hr_manager', 'HR Manager'),
        ('hr_executive', 'HR Executive'),
        ('recruiter', 'Recruiter'),
        ('talent_acquisition_specialist', 'Talent Acquisition Specialist'),
        ('hr_coordinator', 'HR Coordinator'),
        # Finance
        ('finance_manager', 'Finance Manager'),
        ('accountant', 'Accountant'),
        ('senior_accountant', 'Senior Accountant'),
        ('financial_analyst', 'Financial Analyst'),
        ('auditor', 'Auditor'),
        # Marketing
        ('marketing_manager', 'Marketing Manager'),
        ('digital_marketing_executive', 'Digital Marketing Executive'),
        ('seo_specialist', 'SEO Specialist'),
        ('content_strategist', 'Content Strategist'),
        ('social_media_manager', 'Social Media Manager'),
        # Sales
        ('sales_manager', 'Sales Manager'),
        ('sales_executive', 'Sales Executive'),
        ('business_development_executive', 'Business Development Executive'),
        ('sales_coordinator', 'Sales Coordinator'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='development')
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, default='software_engineer')

    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    fathers_name = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)

    # Employment Dates
    join_date = models.DateField(auto_now_add=True)
    date_of_leaving = models.DateField(null=True, blank=True)

    # Contact
    phone = models.CharField(max_length=20, null=True, blank=True)

    # Work Schedule
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = "main_employee_profile"

    def __str__(self):
        return f"{self.employee_id} - {self.user.name}"
