from django.db import models
from .user import User


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sick_leave', 'Sick Leave'),
        ('casual_leave', 'Casual Leave'),
        ('maternity_leave', 'Maternity Leave'),
        ('medical_leave', 'Medical Leave'),
        ('condolences_leave', 'Condolences Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_leave_request'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name} - {self.leave_type} ({self.status})"


class LeaveDocument(models.Model):
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='leave_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'main_leave_document'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Document for {self.leave_request}"
