from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class User(AbstractUser):
    USER_TYPES = [
        ('P', 'Patient'),
        ('D', 'Doctor'),
        ('A', 'Admin'),
        ('N', 'Nurse'),
        ('H', 'Human Resources')
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
    SPEC_TYPES = [
        ('AnatomicalPathology', 'AnatomicalPathology'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Cardiology', 'Cardiology'),
        ('Cardiovascular/ThoracicSurgery', 'Cardiovascular/ThoracicSurgery'),
        ('ClinicalImmunology/Allergy', 'ClinicalImmunology/Allergy'),
        ('CriticalCareMedicine', 'CriticalCareMedicine'),
        ('Dermatology', 'Dermatology'),
        ('DiagnosticRadiology', 'DiagnosticRadiology'),
        ('EmergencyMedicine', 'EmergencyMedicine'),
        ('EndocrinologyandMetabolism', 'EndocrinologyandMetabolism'),
        ('FamilyMedicine', 'FamilyMedicine'),
        ('Gastroenterology', 'Gastroenterology'),
        ('GeneralInternalMedicine', 'GeneralInternalMedicine'),
        ('GeneralSurgery', 'GeneralSurgery'),
        ('General/ClinicalPathology', 'General/ClinicalPathology'),
        ('GeriatricMedicine', 'GeriatricMedicine'),
        ('Hematology', 'Hematology'),
        ('MedicalBiochemistry', 'MedicalBiochemistry'),
        ('MedicalGenetics', 'MedicalGenetics'),
        ('MedicalMicrobiologyandInfectiousDiseases', 'MedicalMicrobiologyandInfectiousDiseases'),
        ('MedicalOncology', 'MedicalOncology'),
        ('Nephrology', 'Nephrology'),
        ('Neurology', 'Neurology'),
        ('Neurosurgery', 'Neurosurgery'),
        ('NuclearMedicine', 'NuclearMedicine'),
        ('Obstetrics/Gynecology', 'Obstetrics/Gynecology'),
        ('OccupationalMedicine', 'OccupationalMedicine'),
        ('Ophthalmology', 'Ophthalmology'),
        ('OrthopedicSurgery', 'OrthopedicSurgery'),
        ('Otolaryngology', 'Otolaryngology'),
        ('Pediatrics', 'Pediatrics'),
        ('PhysicalMedicineandRehabilitation', 'PhysicalMedicineandRehabilitation'),
        ('PlasticSurgery', 'PlasticSurgery'),
        ('Psychiatry', 'Psychiatry'),
        ('PublicHealthandPreventiveMedicine', 'PublicHealthandPreventiveMedicine'),
        ('RadiationOncology', 'RadiationOncology'),
        ('Respirology', 'Respirology'),
        ('Rheumatology', 'Rheumatology'),
        ('Urology', 'Urology'),
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

    type = models.CharField(max_length=2, choices=USER_TYPES, default='P')
    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='S')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_TYPES, default='M')
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    clinic = models.ForeignKey('doctors.Clinic', on_delete=models.CASCADE, null=True, blank=True)
    ssn = models.CharField(max_length=14, unique=True, null=True)
    insurance_number = models.CharField(max_length=9, unique=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPEC_TYPES, null=True)
    blood = models.CharField(max_length=3, choices=BLOOD_TYPES, default='O+', null=True)


class Reservations(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    clinic = models.ForeignKey('doctors.Clinic', on_delete = models.CASCADE, null=True, blank=True)
    working_hour = models.ForeignKey('doctors.WorkingHour', on_delete = models.CASCADE , null=True, blank=True)
    number_in_qeue = models.IntegerField(default=1)

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
    