import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, Room, User

class ChatConsumer(AsyncWebsocketConsumer):
    # Metoda volaná při připojení klienta
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Připojení k real-time skupině pro danou místnost
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Metoda volaná při odpojení klienta
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Metoda volaná při přijetí dat z WebSocketu
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # === Zpracování textové zprávy ===
        if message_type == 'chat_message':
            message = data['message']
            username = self.scope['user'].username
            new_message = await self.save_message(username, self.room_name, message)
            
            today = timezone.now().date()
            timestamp_str = new_message.timestamp.strftime('%H:%M' if new_message.timestamp.date() == today else '%d.%m.%Y')

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message_broadcast',
                    'message': message,
                    'username': username,
                    'timestamp': timestamp_str
                }
            )
        
        # === Zpracování kreslení ===
        elif message_type == 'drawing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'drawing_broadcast',
                    'event': data,
                    'sender_channel': self.channel_name
                }
            )
        
        # === Zpracování mazání plátna ===
        elif message_type == 'clear_canvas':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'clear_canvas_broadcast',
                    'sender_channel': self.channel_name
                }
            )

        # === Zpracování kroku zpět ===
        elif message_type == 'force_redraw':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'redraw_broadcast',
                    'content': data['content'],
                    'sender_channel': self.channel_name
                }
            )

    # --- Metody pro rozesílání zpráv zpět klientům ---

    async def chat_message_broadcast(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

    async def drawing_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['event']))

    async def clear_canvas_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({'type': 'clear_canvas'}))
    
    async def redraw_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'force_redraw',
                'content': event['content']
            }))
            
    # --- Pomocná metoda pro uložení zprávy do databáze ---
    @database_sync_to_async
    def save_message(self, username, room_name, message):
        user = User.objects.get(username=username)
        room, created = Room.objects.get_or_create(name=room_name)
        new_msg_obj = Message.objects.create(author=user, room=room, content=message)
        return new_msg_obj