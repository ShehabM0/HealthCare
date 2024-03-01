from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class User(AbstractUser):
    USER_TYPES = [
        ('P', 'Patient'),
        ('D', 'Doctor'),
        ('A', 'Admin'),
        ('N', 'Nurse'),
    ]
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
    type = models.CharField(max_length=2, choices=USER_TYPES, default='P')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_TYPES, default='M')
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField( null=True, blank=True)
    # phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=STATUS_TYPES, default='S')