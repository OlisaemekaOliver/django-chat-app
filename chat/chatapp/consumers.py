import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )

        await self.accept()

    # ==============================
    # SAVE MESSAGE (with local import)
    # ==============================
    @database_sync_to_async
    def save_message(self, username, text):
        # FIX: Import models inside the method
        from chat.chatapp.models import Conversation, Message
        from django.contrib.auth.models import User

        conversation = get_object_or_404(Conversation, id=self.room_id)
        user = User.objects.get(username=username)

        return Message.objects.create(
            conversation=conversation,
            sender=user,
            text=text
        )

    # ==============================
    # RECEIVE MESSAGE + TYPING
    # ==============================
    async def receive(self, text_data):
        data = json.loads(text_data)

        # ---- Typing indicator ----
        if "typing" in data:
            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "typing_event",
                    "sender": data["sender"],
                    "typing": data["typing"],
                }
            )
            return

        # ---- Actual message ----
        message = data["message"]
        sender = data["sender"]

        await self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender
            }
        )

    # ==============================
    # SEND MESSAGE TO FRONTEND
    # ==============================
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

    # ==============================
    # SEND TYPING EVENT TO FRONTEND
    # ==============================
    async def typing_event(self, event):
        await self.send(text_data=json.dumps({
            "typing": event["typing"],
            "sender": event["sender"]
        }))
