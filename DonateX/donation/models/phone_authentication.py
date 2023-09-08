# models.py
from django.db import models

class OTP(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username