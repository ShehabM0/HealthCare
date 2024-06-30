from .models import ChatMessage, ChatRoom
from rest_framework import serializers
from patients.models import *
  

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['sender', 'message', 'created_at']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'type','clinic'] 


class UserSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','employee']  