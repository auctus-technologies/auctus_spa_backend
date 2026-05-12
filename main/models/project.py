from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_CHOICES = (
        ('Planning', 'Planning'),
        ('Progress', 'Progress'),
        ('Testing', 'Testing'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    )

    name = models.CharField(max_length=255)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='projects')
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planning')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "main_project"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='project_attachments/')
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=100, null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "main_project_attachment"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.project.name} - {self.file_name}"
