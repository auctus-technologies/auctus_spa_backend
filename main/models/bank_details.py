from django.db import models
from .user import User


class BankDetails(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="bank"
    )

    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)

    class Meta:
        db_table = "main_bank_details"

    def __str__(self):
        return f"{self.bank_name} - {self.user.name}"
