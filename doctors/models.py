from django.db import models
from patients.models import User
# Create your models here.


class Clinic(models.Model):
    name = models.CharField(max_length=100)

class WorkingHour(models.Model):
    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
