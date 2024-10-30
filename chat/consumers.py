import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .templatetags.tags import initials
from django.utils.timesince import timesince
from account.models import User
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.user.is_staff:
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'users_update',
            })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if not self.user.is_staff:
            await self.set_room_closed()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        data_type = data['type']
        message = data['message']
        name = data['name']
        agent = data.get('agent', '')

        print(f'Receive: {type}')

        if data_type == 'message':
            new_message = await self.create_message(name, message, agent)
            # send message to group / room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at)
                }
            )
        elif data_type == 'update':
                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'writing_active',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                })

    async def writing_active(self, event):
        await self.send(text_data=json.dumps({
            'type': 'writing_active',
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
        }))

    async def chat_message(self, event):
        # send message to webSocket
        await self.send(
            text_data=json.dumps({
                'type': event['type'],
                'message': event['message'],
                'name': event['name'],
                'agent': event['agent'],
                'initials': event['initials'],
                'created_at': event['created_at']
            })
        )

    async def users_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'users_update'
        }))

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(
            body=message,
            sent_by=sent_by
        )
        if agent:
            message.created_by = User.objects.get(pk=agent)
            message.save()

        self.room.messages.add(message)

        return message

    @sync_to_async
    def set_room_closed(self):
        self.room = Room.objects.get(uuid=self.room_name)
        self.room.status = Room.Status.CLOSED
        self.room.save()
