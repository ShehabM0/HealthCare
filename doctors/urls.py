from django.urls import path
from .views import *


app_name = 'doctors'

urlpatterns = [
    path('clinics/', ListAllClinics.as_view()),
    # path('clinic/<int:pk>/', ClinicView.as_view()),
    # path('clinic/', AddClinicView.as_view()),
    path('working-hours/<int:clinic_id>', GetClinicWorkingHours.as_view()),
    # path('working-hour/', AddWorkingHourView.as_view()),
    # path('working-hour/<int:pk>/', WorkingHoursView.as_view()),
    path('clinic/<int:clinic_id>/status/', UpdateClinicStatus.as_view()),
]