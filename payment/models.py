from patients.models import User
from django.db import models

class CreditCard(models.Model):
    number = models.CharField(max_length=16, unique=True)
    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()
    cvv = models.PositiveSmallIntegerField()
    balance = models.IntegerField()

    def __str__(self):
        ls=[self.number[i:i+4] for i in range(0, len(self.number), 4)]
        res=ls[0]
        for i in ls:res+=" "+i
        return res

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    remember_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.user} - {self.card}"

class Purchase(models.Model):
    PAYMENT_TYPES = [
        ('reservation', 'reservation'),
        ('pharmacy', 'pharmacy')
    ]
    payment_type = models.CharField(max_length=32, choices=PAYMENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    success = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_type} : {self.user} - {self.success}"
