import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["sender"]

        # Buscar al usuario que envia el mensaje
        sender = await self.get_user(sender_username)

        # Buscar la sala de chat (o crear una si no existe)
        chatroom, created = await self.get_or_create_chatroom(self.room_name)

        # Guardar el mensaje en la BD
        msg = Message.objects.create(chatroom=chatroom, sender=sender, message=message)

        # Enviar el mensaje a todos los clientes conectados
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.message,
                "sender": sender.username,
                "timestamp": str(msg.timestamp)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"]
        }))

    @staticmethod
    async def get_user(username):
        """ Obtiene un usuario por su username """
        return await User.objects.aget(username=username)

    @staticmethod
    async def get_or_create_chatroom(room_name):
        """ Obtiene o crea una sala de chat """
        chatroom, created = await ChatRoom.objects.aget_or_create(room_name=room_name)
        return chatroom, created
