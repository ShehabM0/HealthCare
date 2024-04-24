from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatRoomSerializer
from .models import ChatRoom, ChatMessage
from rest_framework import status
from django.db.models import Q
from .serializers import *

@api_view(['GET'])
def ListRoomsView(req):
    user = req.user
    rooms = user.chat_rooms.all()
    serializer = ChatRoomSerializer(rooms, many=True)

    return Response({"message": serializer.data})

@api_view(['POST'])
def CreateRoomView(req):
    sender = req.user
    if not sender.is_authenticated:
        return Response({"message": "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    receiver = req.data.get('other_user', None)

    try:
        receiver = User.objects.get(username=receiver)
    except User.DoesNotExist:
        return Response({"message": "User Doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)

    room_format1 = f"{sender}-{receiver}"
    room_format2 = f"{receiver}-{sender}"
    get_room = ChatRoom.objects.filter(
        Q(room_name = room_format1) |
        Q(room_name = room_format2)
    )
    if get_room.exists():
        return Response({"message": "Room already exist!!"}, status=status.HTTP_409_CONFLICT)

    room = ChatRoom.objects.create(room_name = room_format1)
    room.users.add(sender, receiver)
    serializer = ChatRoomSerializer(room, many=False)

    return Response({"message": "Room created successfully.", "data": serializer.data})

@api_view(['GET'])
def ListRoomMessagesView(req):
    user = req.user
    room_name = req.data.get('room_name', None)

    try:
        room = ChatRoom.objects.get(room_name = room_name)
        messages = ChatMessage.objects.filter(room = room)
    except ChatRoom.DoesNotExist:
        return Response({"message": "Room doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatMessageSerializer(messages, many=True)

    return Response({"data": serializer.data})
