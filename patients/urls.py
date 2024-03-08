from django.urls import path
from . import views
from rest_framework import permissions


app_name = 'patients'

urlpatterns = [
    path('register/', views.Register_view.as_view(), name='register'),
    path('reserve-clinic/', views.ReserveClinicView.as_view(), name='reserve-clinic'),
    path('reservations/', views.ReservationsView.as_view(), name='reservations'),
    path('upload-record/', views.UploadMedicalRecord.as_view(), name='upload-record'),
]