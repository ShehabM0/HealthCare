from django.db import models
from django.utils import timezone

class VerificationCode(models.Model):
    OP_TYPES = [
        ('forgot-password', 'forgot-password'),
        ('change-email', 'change-email'),
        ('register', 'register'),
    ]
    type = models.CharField(max_length=15, choices=OP_TYPES)
    email = models.EmailField()
    code = models.CharField(max_length=40)
    created_at = models.CharField(max_length=30, default=f' {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    def __str__(self):
        return self.email + " - " + self.code
