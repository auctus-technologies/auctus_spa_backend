from django.db import models
from django.conf import settings


class Notification(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title       = models.CharField(max_length=255)
    message     = models.TextField()
    notif_type  = models.CharField(max_length=50, default='task_assigned')
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'main_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.name} — {self.title}'
