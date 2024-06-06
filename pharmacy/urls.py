from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('medications/<int:medication_id>/related/', views.ListRelatedMedications, name = 'list-related-medications'),
    path('medications/', views.ListMedications, name = 'list-medications'),

    path('add-prescription/<int:patient_id>/', views.CreatePrescription, name = 'create-patient-prescription'),
    path('clear-prescription/<int:prescription_id>/', views.ClearPrescription, name = 'clear-prescription'),

    path('prescription/<int:prescription_id>/item/', views.AddToPrescription, name = 'add-to-prescription'),
    path('prescription/<int:prescription_id>/item/<int:prescription_item_id>/', views.RemoveFromPrescription, name = 'remove-from-prescription'),

    path('prescriptions/<int:patient_id>/', views.ListPatientPrescriptions, name = 'list-patient-prescriptions'),
    path('prescription/<int:prescription_id>/items/', views.ListPrescriptionItems, name = 'list-patient-prescription-items'),

    path('add-purchase/<int:prescription_id>/', views.AddPrescriptionPurchase, name='add-prescription-purchase'),
]

