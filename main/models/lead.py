from django.db import models
from django.conf import settings


class Lead(models.Model):
    STATUS_CHOICES = (
        ('proposal', 'Proposal'),
        ('sent', 'Sent'),
        ('processing', 'Processing'),
        ('client', 'Client'),
        ('lost', 'Lost'),
        ('not_interested', 'Not Interested'),
    )

    LEAD_FROM_CHOICES = (
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('meta_ads', 'Meta Ads'),
        ('linkedin', 'LinkedIn'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter'),
        ('other', 'Other'),
    )

    client_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    lead_from = models.CharField(max_length=20, choices=LEAD_FROM_CHOICES, blank=True, null=True)
    lead_date = models.DateField(blank=True, null=True)
    follow_up_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='follow_up_leads',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_lead'
        ordering = ['-created_at']

    def __str__(self):
        return self.client_name
