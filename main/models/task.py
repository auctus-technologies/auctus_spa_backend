from django.db import models
from django.conf import settings
from .project import Project


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='assigned_tasks', blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tasks'
    )
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_task'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
