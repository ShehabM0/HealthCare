from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('create-user/', views.CreateUserView, name = 'create-user'),
    path('list/', views.ListEmployeesView, name = 'list-employees'),
    path('list/<str:type>/', views.ListEmployeesView, name = 'list-employees-type'),
]

