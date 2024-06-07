from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, ChatMessage
from patients.models import User
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            print("User not authenticated!!")
            return
        
        try:
            self.room = ChatRoom.objects.get(room_name = self.room_name)
        except ChatRoom.DoesNotExist:
            print("Room Doesn't Exist!!")
            return

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        req = json.loads(text_data)
        
        type = req['type']
        message = req['message']

        event = {
            'type': type,
            'message': message
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            event
        )

    def send_message(self, event):
        message = event['message']

        ChatMessage.objects.create(
            room = self.room,
            sender = self.user,
            message = message,
        )

        self.send(
            text_data=json.dumps({
                'type': 'send_message',
                'message': message,
                'user': self.user.username
        }))

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

'''
let webSocket = new WebSocket('ws/connection/');
webSocket.onmessage = function(e) { console.log(e.data) }
webSocket.send(JSON.stringify({ 'type': 'send_req', 'data': 'ping' }))
'''
