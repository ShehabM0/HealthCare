from patients.models import User
from django.db import models

class MedicationCategory(models.Model):
    category = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "Medication Categories"

    def __str__(self):
        return self.category

class Medication(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='media/medications/', blank=True, null=True)
    cost = models.PositiveSmallIntegerField()
    available = models.BooleanField()
    category = models.ManyToManyField(MedicationCategory)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} - {self.available}"

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions_written')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions_received')
    created_at = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False) # toggle

    def __str__(self):
        return f"{self.doctor} - {self.patient}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='items', on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    instructions = models.TextField(blank=True, null=True) # [dose] for [duration/period]

    def __str__(self):
        return f"{self.prescription} - {self.medication.name}"

