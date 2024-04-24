from .models import ChatMessage, ChatRoom
from rest_framework import serializers
from patients.models import User

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
