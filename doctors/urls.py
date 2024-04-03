from django.urls import path
from .views import *


app_name = 'doctors'

urlpatterns = [
    path('doctors/', ListDoctorsView.as_view()),
    path('clinics/', ListClinicsView.as_view()),
    path('clinic/<int:pk>/', ClinicView.as_view()),
    path('clinic/', AddClinicView.as_view()),
    path('working-hours/', AddWorkingHourView.as_view()),
    path('working-hour/<int:pk>/', WorkingHoursView.as_view()),
]