from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('medications/<int:medication_id>/related/', views.ListRelatedMedications, name = 'list-related-medications'),
    path('medications/', views.Medications, name = 'list-medications'),
    path('medications/', views.AddMedication, name='add-new-medication'),
    path('medications/<int:medication_id>/categories/<int:category_id>/', views.MedicationCategories, name='add-category-to-medicaiton'),
    path('medications/<int:medication_id>/categories/<int:category_id>/', views.MedicationCategories, name='add-category-to-medicaiton'),
    path('medications/<int:medication_id>/', views.MedicationsID, name='get-medication'),
    path('medications/<int:medication_id>/', views.MedicationsID, name='update-medication'),
    path('medications/categories/', views.Categories, name='add-new-category'),
    path('medications/categories/', views.Categories, name='list-categories'),

    path('add-prescription/<int:patient_id>/', views.CreatePrescription, name = 'create-patient-prescription'),
    path('clear-prescription/<int:prescription_id>/', views.ClearPrescription, name = 'clear-prescription'),

    path('prescriptions/<int:prescription_id>/items/', views.PrescriptionsItems, name = 'add-to-prescription'),
    path('prescriptions/<int:prescription_id>/items/<int:prescription_item_id>/', views.RemoveFromPrescription, name = 'remove-from-prescription'),
    path('prescriptions/<str:patient_username>/', views.ListPatientPrescriptions, name = 'list-patient-prescriptions'),
    path('prescriptions/<int:prescription_id>/items/', views.PrescriptionsItems, name = 'list-patient-prescription-items'),
    path('prescriptions/<int:prescription_id>/verify-purchase/', views.VerifyPrescriptionPurchase, name='verift-prescription-purchase'),

    path('add-purchase/<int:prescription_id>/', views.AddPrescriptionPurchase, name='add-prescription-purchase'),

]

