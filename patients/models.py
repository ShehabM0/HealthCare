from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from hr.models import Employee
from django.db import models

class User(AbstractUser):
    GENDER_TYPES = [
        ('M', 'Male'),
        ('F' , 'Female'),
    ]
    STATUS_TYPES = [
        ('M', 'Maried'),
        ('S','Single'),
        ('W','widow'),
        ('D','devorced')
    ]
    BLOOD_TYPES = [
        ('O', 'O'),
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('AB-', 'AB-'),
        ('AB+', 'AB+'),
    ]

    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='S')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_TYPES, default='M')
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    clinic = models.ForeignKey('doctors.Clinic', on_delete=models.CASCADE, null=True, blank=True)
    ssn = models.CharField(max_length=14, unique=True, null=True)
    insurance_number = models.CharField(max_length=9, unique=True, null=True)
    blood = models.CharField(max_length=3, choices=BLOOD_TYPES, default='O+', null=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True)

class Reservation(models.Model):
    statuses = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Done'),
    ]
    TYPES = [
        (   'S' , 'Surgery'),
        (   'C' , 'Consultation'),
        (   'V' , 'Visit'),
        (   'E' , 'Examination'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    clinic = models.ForeignKey('doctors.Clinic', on_delete = models.CASCADE, null=True, blank=True)
    working_hour = models.ForeignKey('doctors.WorkingHour', on_delete = models.CASCADE , null=True, blank=True)
    number_in_qeue = models.IntegerField(default=1)
    status = models.CharField(max_length=1, choices=statuses, default='P')
    price = models.FloatField(default=100)
    reserved_at = models.CharField(max_length=30, default=f'{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
    payment = models.CharField(max_length=100, default='Cash')
    payment_status = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=TYPES, default='C')

class MedicalHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_history')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    disease = models.CharField(max_length=100)
    treatment = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

class MedicalRecord(models.Model):
    FILE_TYPES = [
        ('P', 'Prescription'),
        ('R', 'Report'),
        ('I', 'Image'),
        ('A', 'Analysis'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_record')
    file = models.FileField(upload_to='medical_records', null=True, blank=True)
    type = models.CharField(max_length=1, choices=FILE_TYPES, default='P')
    