from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('list-room-messages/<str:room_name>/', ListRoomMessagesView, name='list-room-messages'),
    path('list-my-rooms/', ListRoomsView, name='list-all-user-rooms'),
    path('create-room/', CreateRoomView, name='create-new-room'),

    path('ws/', wsTemplate)
]
