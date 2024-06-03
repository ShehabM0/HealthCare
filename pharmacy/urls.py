from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('list-related-medications/<int:medication_id>/', views.ListRelatedMedications, name = 'list-related-medications'),
    path('list-medications/', views.ListMedications, name = 'list-medications'),

    path('create-prescription/<int:patient_id>/', views.CreatePrescription, name = 'create-patient-prescription'),
    path('add-to-prescription/<int:prescription_id>/', views.AddToPrescription, name = 'add-to-prescription'),
    path('remove-from-prescription/<int:prescription_item_id>/', views.RemoveFromPrescription, name = 'add-to-prescription'),
    path('clear-prescription/<int:prescription_id>/', views.ClearPrescription, name = 'add-to-prescription'),

    path('add-purchase/<int:prescription_id>/', views.AddPrescriptionPurchase, name='add-prescription-purchase'),

    path('patient-prescriptions/<int:patient_id>/', views.ListPatientPrescriptions, name = 'list-patient-prescriptions'),
    path('patient-prescription-items/<int:prescription_id>/', views.ListPrescriptionItems, name = 'list-patient-prescription-items'),
]

