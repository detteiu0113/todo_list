import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import TodoItem
from accounts.models import CustomUser

class TodoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'todo'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        title = text_data_json.get('title')
        user_id = text_data_json.get('user_id')
        todo_id = text_data_json.get('todo_id')
        completed = text_data_json.get('completed')

        if type == 'add':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'add',
                    'title': title,
                    'user_id': user_id,
                    'todo_id': todo_id
                }
            )
            await self.add_todo(todo_id, title, user_id)

        elif type == 'complete':
            await self.channel_layer.group_send(    
                self.group_name,
                {
                    'type': 'complete',
                    'todo_id': todo_id,
                    'completed': completed
                }
            )
            await self.complete_todo(todo_id, completed)

        elif type == 'edit':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'edit',
                    'title': title,
                    'todo_id': todo_id
                }
            )
            await self.edit_todo(todo_id, title)

        elif type == 'move':
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'move',
                    'todo_id': todo_id,
                    'user_id': user_id,
                }
            )
            await self.move_todo(todo_id, user_id)

    async def add(self, event):
        title = event['title']
        user_id = event['user_id']
        todo_id = event['todo_id']

        await self.send(text_data=json.dumps({
            'type': 'add',
            'title': title,
            'user_id': user_id,
            'todo_id': todo_id
        }))

    async def complete(self, event):
        todo_id = event['todo_id']
        completed = event['completed']

        await self.send(text_data=json.dumps({
            'type': 'complete',
            'todo_id': todo_id,
            'completed': completed
        }))

    async def edit(self, event):
        title = event['title']
        todo_id = event['todo_id']

        await self.send(text_data=json.dumps({
            'type': 'edit',
            'title': title,
            'todo_id': todo_id
        }))

    async def move(self, event):
        todo_id = event['todo_id']
        user_id = event['user_id']

        await self.send(text_data=json.dumps({
            'type': 'move',
            'todo_id': todo_id,
            'user_id': user_id
        }))


    @database_sync_to_async
    def add_todo(self, todo_id, title, user_id):
        if user_id:
            TodoItem.objects.create(id=todo_id, title=title, completed=False, user_id=user_id)
        else:
            TodoItem.objects.create(id=todo_id, title=title, completed=False)

    @database_sync_to_async
    def complete_todo(self, todo_id, completed):
        todo_item = TodoItem.objects.get(id=todo_id)
        todo_item.completed = completed
        todo_item.save()

    @database_sync_to_async
    def edit_todo(self, todo_id, title):
        todo_item = TodoItem.objects.get(id=todo_id)
        todo_item.title = title
        todo_item.save()

    @database_sync_to_async
    def move_todo(self, todo_id, user_id):
        todo_item = TodoItem.objects.get(id=todo_id)
        if user_id:
            user = CustomUser.objects.get(id=user_id)
        else:
            user = None
        todo_item.user = user
        todo_item.save()