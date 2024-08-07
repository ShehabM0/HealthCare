from django.db import models
# Create your models here.


class Clinic(models.Model):
    statuses = [
        ('A', 'Available'),
        ('C', 'Closed'),
    ]
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=statuses, default='A')
    price = models.FloatField(default=100)


class WorkingHour(models.Model):
    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True, related_name='working_hours')
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()