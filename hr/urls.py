from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('create-employee/', views.CreateEmployeeView, name = 'create-employee'),
    path('update-employee/<int:pk>/', views.UpdateEmployeeView, name = 'update-employee'),
]

