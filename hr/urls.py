from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('create-user/', views.CreateUserView, name = 'create-user'),
    path('list/', views.ListEmployeesView, name = 'list-employees'),
    path('list/<str:type>/', views.ListEmployeesView, name = 'list-employees-by-type'),
    path('profile/<int:pk>/', views.GetProfile, name = 'get-employee-by-id'),
]

