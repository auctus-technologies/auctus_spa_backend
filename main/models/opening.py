from django.db import models
from .employee_profile import EmployeeProfile


class JobOpening(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=50, choices=EmployeeProfile.DEPARTMENT_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=50, choices=EmployeeProfile.DESIGNATION_CHOICES, null=True, blank=True)
    qualification_required = models.CharField(max_length=255, null=True, blank=True)
    required_experience = models.PositiveIntegerField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    skills_required = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_job_opening'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job_title} - {self.department or '-'}"
