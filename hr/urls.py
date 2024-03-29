from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('create-user/', views.CreateUserView, name = 'create-user'),
]

