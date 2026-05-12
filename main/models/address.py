from django.db import models
from .user import User


class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "main_address"

    def __str__(self):
        return f"{self.city}, {self.country} - {self.user.name}"
