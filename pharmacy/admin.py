from .models import Prescription, PrescriptionItem, MedicationCategory, Medication 
from django.contrib import admin

admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(MedicationCategory)
admin.site.register(Medication)
