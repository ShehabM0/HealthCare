from django.urls import path
from . import views
from rest_framework import permissions

app_name = 'nurses'

urlpatterns = [
    path('profile/', views.GetProfile.as_view(), name='profile'),
    path('Casses/', views.GetPatientsClinic.as_view(), name='Casses'),
    path('Room/<int:room_id>', views.GetRoom.as_view(), name='Room'),
    # path('Bed/', views.GetBed.as_view(), name='Bed'),
    path('AllRooms/', views.GetAllRooms.as_view(), name='AllRooms'),
    path('Calls/', views.GetCalls.as_view(), name='Calls'),
    path('AllCalls/', views.GetAllCalls.as_view(), name='AllCalls'),
    # path('/', views.GetRoomReservation.as_view(), name=''),
    # path('/', views.GetRoomReservation.as_view(), name=''),
    # path('/', views.GetRoomReservation.as_view(), name=''),
    # path('/', views.GetRoomReservation.as_view(), name=''),
]
