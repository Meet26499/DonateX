from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('success', 'Success'),
    ('reject', 'Reject'),
    ('pending', 'Pending'),
)

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} donated {self.amount}"
