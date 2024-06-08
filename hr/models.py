from django.db import models
from doctors.models import Clinic

class Employee(models.Model):
    USER_TYPES = [
        ('D', 'Doctor'),
        ('A', 'Admin'),
        ('N', 'Nurse'),
        ('H', 'Human Resources')
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
    ]

    type = models.CharField(max_length=2, choices=USER_TYPES, default='P')
    specialization = models.CharField(max_length=50, choices=SPECIALIZAION_TYPES, null=True)
    salary = models.PositiveIntegerField(null=True)
    hired_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        type_full_str = None
        if self.type == 'D': type_full_str = "Doctor"
        elif self.type == 'N': type_full_str = "Nurse"
        elif self.type == 'H': type_full_str = "Human Resource"
        return f"{type_full_str} - {self.specialization}"
