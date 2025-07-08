# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Získá název místnosti z URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Připojí se ke skupině specifické pro danou místnost
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Odpojí se od skupiny
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Přijme zprávu z WebSocketu
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username

        # Uloží zprávu do databáze
        await self.save_message(username, self.room_name, message)

        # Rozešle zprávu do skupiny dané místnosti
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Přijme zprávu z room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Pošle zprávu zpět do WebSocketu (do prohlížeče)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        user = User.objects.get(username=username)
        # Najde místnost podle jména, nebo ji vytvoří, pokud neexistuje
        room, created = Room.objects.get_or_create(name=room_name)
        
        Message.objects.create(author=user, room=room, content=message)