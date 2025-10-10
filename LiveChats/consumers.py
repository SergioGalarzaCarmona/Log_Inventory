import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import LiveChat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Fetch the chat object once during connection
        try:
            self.chat = await self.get_chat()
        except LiveChat.DoesNotExist:
            # If chat doesn't exist, reject connection
            await self.close()
            return

        # Join chat group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        user = self.scope.get("user")

        if not message or not user or not user.is_authenticated:
            return 

        timestamp = timezone.now().strftime("%H:%M")
        
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'timestamp': timestamp,
            }
        )
        
        asyncio.create_task(self.save_message(self.chat, user, message))

    async def chat_message(self, event):
        """
        Send message to WebSocket client
        """
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    # ---------- Database operations ----------
    @database_sync_to_async
    def get_chat(self):
        return LiveChat.objects.get(id=self.chat_id)

    @database_sync_to_async
    def save_message(self, chat, user, text):
        try:
            return Message.objects.create(chat=chat, sender=user, text=text)
        except Exception as e:
            # Log error in production
            print(f"Error saving message: {e}")
            return None
