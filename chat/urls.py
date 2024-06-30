from django.urls import path
from .views import *
from . import views

app_name = 'chat'

urlpatterns = [
    path('list-room-messages/<str:room_name>/', ListRoomMessagesView, name='list-room-messages'),
    path('list-my-rooms/', ListRoomsView, name='list-all-user-rooms'),
    path('create-room/', CreateRoomView, name='create-new-room'),
    path('Chat/Doctors/', views.GetDoctorsNumber.as_view(), name='GetDoctorsNumber'),
    path('ws/', wsTemplate)
]
