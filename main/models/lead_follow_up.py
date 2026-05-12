from django.db import models
from django.conf import settings


class LeadFollowUp(models.Model):
    lead = models.ForeignKey(
        'main.Lead',
        on_delete=models.CASCADE,
        related_name='follow_ups',
    )
    follow_up_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_follow_ups',
    )
    follow_up_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_lead_follow_up'
        ordering = ['-follow_up_date', '-created_at']

    def __str__(self):
        return f"Follow-up for {self.lead} on {self.follow_up_date}"
