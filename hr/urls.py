from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('employee/', views.EmployeeView, name = 'create-employee'),
    path('employee/', views.EmployeeView, name = 'update-employee'),
    path('employee/<int:pk>/', views.UpdateEmployeeByIDView, name = 'update-employee-by-id'),
]

