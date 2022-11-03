import json


from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
now = timezone.localtime()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 파라미터 값으로 채팅 룸을 구별
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # 룸 그룹에 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()



    async def disconnect(self, close_code):
        # 룸 그룹 나가기
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)




    async def receive(self, text_data):
        # 웹소켓에게 메시지 받음
        username = self.scope["user"].nickname # 웹소켓에서 닉네임 가져와서 저장
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # timestamp = timezone.now().isoformat()
        message = (username + ': ' + message)

        # 룸그룹에게 메시지 보냄
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "user": username
            }
        )



    async def chat_message(self, event):
        # 룸그룹에게 메시지 받음
        username = self.scope["user"].username
        message = event["message"]

        # 웹소켓에게 메시지 보냄
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timezone.now().isoformat()
        }))