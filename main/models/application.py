from django.db import models
from .opening import JobOpening


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('on_hold',  'On Hold'),
    ]

    opening       = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    full_name     = models.CharField(max_length=255)
    email         = models.EmailField()
    phone         = models.CharField(max_length=30, null=True, blank=True)
    city          = models.CharField(max_length=100, null=True, blank=True)
    experience    = models.PositiveIntegerField(null=True, blank=True)
    resume        = models.FileField(upload_to='resumes/', null=True, blank=True)
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    applied_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_job_application'
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} → {self.opening.job_title if self.opening else 'General'}"
