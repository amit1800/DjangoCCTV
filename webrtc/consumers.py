import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class P2PConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "test"
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(text_data=json.dumps({"text": "you are connected"}))

    def receive(self, text_data):
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "broadcastEmit",
                "message": text_data,
                "sender_channel_name": self.channel_name,
            },
        )

    def broadcastEmit(self, event):
        message = event["message"]
        if self.channel_name != event["sender_channel_name"]:
            self.send(text_data=message)


class serverToPeerWS(WebsocketConsumer):
    def connect(self):
        self.group_name = "test"
        self.accept()
        # async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(text_data=json.dumps({"text": "you are to ws 2"}))
