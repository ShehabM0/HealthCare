from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(
            text_data=json.dumps({
                'type': 'test_connection',
                'data': 'Connected!!'
        }))

    def receive(self, text_data):
        req = json.loads(text_data)
        print(req)


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