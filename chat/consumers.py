# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room
from django.contrib.auth.models import User
from django.utils import timezone

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

            new_message = await self.save_message(username, self.room_name, message)
            
            # Zjistíme, jestli je datum zprávy dnešní
            today = timezone.now().date()
            if new_message.timestamp.date() == today:
                # Pokud ano, pošleme jen čas
                timestamp_str = new_message.timestamp.strftime('%H:%M')
            else:
                # Pokud ne, pošleme datum
                timestamp_str = new_message.timestamp.strftime('%d.%m.%Y')

            # Rozešleme zprávu do skupiny s upraveným časem
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': timestamp_str
                }
            )
    
    # Přijme zprávu z room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Pošle zprávu zpět do WebSocketu (do prohlížeče)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room, created = Room.objects.get_or_create(name=room)
        
        new_msg_obj = Message.objects.create(author=user, room=room, content=message)
        return new_msg_obj # PŘIDÁNO