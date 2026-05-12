from django.db import models
from .user import User


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('leave', 'Leave'),
        ('holiday', 'Holiday'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')

    check_in_photo = models.ImageField(upload_to='attendance/checkin/', null=True, blank=True)
    check_out_photo = models.ImageField(upload_to='attendance/checkout/', null=True, blank=True)
    check_in_address = models.TextField(null=True, blank=True)
    check_out_address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "main_attendance"
        unique_together = ["user", "date"]

    def __str__(self):
        return f"{self.user.name} - {self.date} ({self.status})"
