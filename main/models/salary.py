from django.db import models
from .user import User


class Salary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='salary')

    # Earnings
    basic             = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hra               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    da                = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    travel_allowance  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowance   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Deductions
    pf               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi              = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tds              = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deduction  = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    effective_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_salary'

    def __str__(self):
        return f"Salary – {self.user.name}"
