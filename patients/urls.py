from django.urls import path
from . import views
from rest_framework import permissions


app_name = 'patients'

urlpatterns = [
    path('register/', views.Register_view.as_view(), name='register'),
]