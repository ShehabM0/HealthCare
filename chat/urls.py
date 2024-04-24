from django.urls import path
from .views import *

urlpatterns = [
    path('list-room-messages/', ListRoomMessagesView, name='list-room-messages'),
    path('list-rooms/', ListRoomsView, name='list-all-user-rooms'),
    path('create-room/', CreateRoomView, name='create-new-room')
]