from patients.models import User
from django.db import models

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms', blank=True)

    def __str__(self):
        return self.room_name
    

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=None)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.room_name}: {self.sender} - {self.message}"

