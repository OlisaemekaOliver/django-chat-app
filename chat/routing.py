from django.urls import path, re_path
from chat.chatapp.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<conversation_id>\d+)/$", ChatConsumer.as_asgi()),
]
