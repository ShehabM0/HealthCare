from .consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/connection/', ChatConsumer.as_asgi())
]
