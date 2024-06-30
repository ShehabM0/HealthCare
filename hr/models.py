from django.db import models
from doctors.models import Clinic

class Employee(models.Model):
    USER_TYPES_DICT = {
        'A': 'Admin',
        'D': 'Doctor',
        'N': 'Nurse',
        'H': 'Human Resources',
        'P': 'Pharmacist',
        'HD': 'Head Doctor',
        'HN': 'Head Nurse'
    }

    USER_TYPES = [
        ('A', 'Admin'),

        ('D', 'Doctor'),
        ('N', 'Nurse'),
        ('H', 'Human Resources'),
        ('P', 'Pharmacist'),

        ('HD', 'Head Doctor'),    
        ('HN', 'Head Nurse'),
    ]

    SPECIALIZAION_TYPES = [
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
        ('Pharmacist', 'Pharmacist'),
        ('Human Resources', 'Human Resources' ),
    ]

    type = models.CharField(max_length=2, choices=USER_TYPES, default='P')
    specialization = models.CharField(max_length=50, choices=SPECIALIZAION_TYPES, null=True)
    salary = models.PositiveIntegerField(null=True)
    hired_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        type_full_str = self.USER_TYPES_DICT[self.type]
        return f"{type_full_str} - {self.specialization}"
