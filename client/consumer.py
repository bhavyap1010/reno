import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chatroom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "delete":
            message_id = data.get("message_id")
            sender = self.scope['user']
            result = await self.delete_message(message_id, sender)
            if result:
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "deleteMessage",
                        "message_id": message_id,
                    }
                )
            return

        message = data["message"]
        username = data["username"]
        time = data["time"]

        room = await self.get_room(self.room_name)
        sender = self.scope['user']

        if room:
            msg_obj = await self.save_message(room, sender, message)
            message_id = msg_obj.id if msg_obj else None
        else:
            print(f"[ERROR] Chatroom '{self.room_name}' not found — message not saved.")
            message_id = None

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "time": time,
                "message_id": message_id,
            }
        )

    async def sendMessage(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "time": event["time"],
            "message_id": event.get("message_id"),
        }))

    async def deleteMessage(self, event):
        await self.send(text_data=json.dumps({
            "action": "delete",
            "message_id": event["message_id"],
        }))

    @database_sync_to_async
    def get_room(self, room_name):
        return Chatroom.objects.filter(room_name=room_name).first()

    @database_sync_to_async
    def save_message(self, room, sender, content):
        return Message.objects.create(room=room, sender=sender, content=content)

    @database_sync_to_async
    def delete_message(self, message_id, sender):
        from .models import Message
        try:
            msg = Message.objects.get(id=message_id, sender=sender)
            msg.deleted = True
            msg.save()
            return True
        except Message.DoesNotExist:
            return False
