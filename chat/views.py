from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .serializers import ChatRoomSerializer
from .models import ChatRoom, ChatMessage
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from .serializers import *
from rest_framework import status, permissions
from rest_framework.views import APIView

def wsTemplate(req):
    return render(req, 'ws-conn-test.html')

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListRoomsView(req):
    user = req.user
    rooms = user.chat_rooms.all()
    serializer = ChatRoomSerializer(rooms, many=True)

    return Response({"message": serializer.data})

@swagger_auto_schema(method='POST', manual_fields=['other_user'])
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

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def ListRoomMessagesView(req, room_name):
    print(room_name)
    try:
        room = ChatRoom.objects.get(room_name = room_name)
        messages = ChatMessage.objects.filter(room = room)
    except ChatRoom.DoesNotExist:
        return Response({"message": "Room doesn't exist!!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatMessageSerializer(messages, many=True)

    return Response({"data": serializer.data})


class GetDoctorsNumber(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):
        try:
            employees=Employee.objects.filter(type='D')
        except employees.DoesNotExist:
            return Response({"message": "there is no doctors "}, status=404)

        res=[]
        for employee in employees:
           res.append(User.objects.get(employee=employee))

        serializer = UserSerializer(res, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)}) 
    

class GetPatiantNumber(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req):

        users = User.objects.all()
        res=[]
        for user in users :
            if  user.employee is None:
                res.append(user)
        serializer = UserSerializer(res, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data)}) 

