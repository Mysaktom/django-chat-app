import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, Room, User
from django.core.cache import cache
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    # Metoda volaná při připojení klienta
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Připojení ke skupině
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Přidáme uživatele do seznamu online a rozešleme aktualizaci
        await self.add_user_to_online_list()
        await self.broadcast_online_users()

    # Metoda volaná při odpojení klienta
    async def disconnect(self, close_code):
        # Odebereme uživatele ze seznamu online a rozešleme aktualizaci
        await self.remove_user_from_online_list()
        await self.broadcast_online_users()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Metoda volaná při přijetí dat z WebSocketu
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = data['message']
            await self.process_chat_message(message)
        
        elif message_type == 'typing_started':
            await self.broadcast_typing_status(is_typing=True)
        
        elif message_type == 'drawing':
            await self.broadcast_drawing_data(data)
        
        elif message_type == 'clear_canvas':
            await self.broadcast_clear_canvas()

        elif message_type == 'force_redraw':
            await self.broadcast_force_redraw(data['content'])

    # --- Zpracování jednotlivých typů událostí ---

    async def process_chat_message(self, message):
        new_message = await self.save_message(self.user.username, self.room_name, message)
        today = timezone.now().date()
        timestamp_str = new_message.timestamp.strftime('%H:%M' if new_message.timestamp.date() == today else '%d.%m.%Y')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_broadcast',
                'message': message, 'username': self.user.username, 'timestamp': timestamp_str
            }
        )

    async def broadcast_typing_status(self, is_typing):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator_broadcast', 'username': self.user.username,
                'is_typing': is_typing, 'sender_channel': self.channel_name
            }
        )

    async def broadcast_drawing_data(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'drawing_broadcast', 'event': data, 'sender_channel': self.channel_name}
        )

    async def broadcast_clear_canvas(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'clear_canvas_broadcast', 'sender_channel': self.channel_name}
        )
    
    async def broadcast_force_redraw(self, content):
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'redraw_broadcast', 'content': content, 'sender_channel': self.channel_name}
        )

    # --- Metody pro rozesílání zpráv zpět klientům ---

    async def chat_message_broadcast(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message', 'message': event['message'],
            'username': event['username'], 'timestamp': event['timestamp']
        }))

    async def drawing_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['event']))

    async def clear_canvas_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({'type': 'clear_canvas'}))
    
    async def redraw_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({'type': 'force_redraw', 'content': event['content']}))

    async def typing_indicator_broadcast(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator', 'username': event['username'], 'is_typing': event['is_typing']
            }))

    async def user_list_broadcast(self, event):
        await self.send(text_data=json.dumps({'type': 'user_list_update', 'users': event['users']}))


    # --- Pomocné metody pro práci s online uživateli a databází ---
    
    def get_online_users_cache_key(self):
        return f"online_users_{self.room_name}"

    @database_sync_to_async
    def add_user_to_online_list(self):
        online_users = cache.get(self.get_online_users_cache_key(), set())
        online_users.add(self.user.username)
        cache.set(self.get_online_users_cache_key(), online_users, timeout=None)

    @database_sync_to_async
    def remove_user_from_online_list(self):
        online_users = cache.get(self.get_online_users_cache_key(), set())
        online_users.discard(self.user.username)
        cache.set(self.get_online_users_cache_key(), online_users, timeout=None)

    async def broadcast_online_users(self):
        online_users_set = await database_sync_to_async(cache.get)(self.get_online_users_cache_key(), set())
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_list_broadcast', 'users': sorted(list(online_users_set))}
        )

    @database_sync_to_async
    def save_message(self, username, room_name, message):
        user = User.objects.get(username=username)
        room, created = Room.objects.get_or_create(name=room_name)
        new_msg_obj = Message.objects.create(author=user, room=room, content=message)
        return new_msg_obj