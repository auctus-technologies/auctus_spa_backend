from django.db import models


class Holiday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "main_holiday"
        ordering = ['date']

    def __str__(self):
        return self.name
