import json
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync
import asyncio
import logging
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
    RTCIceServer,
    RTCConfiguration,
)
from webrtc.customVideoTrack import CustomVideoTrack

logger = logging.getLogger("pc")


class serverToPeerWS(WebsocketConsumer):
    def connect(self):
        ice_server = RTCIceServer(
            urls=["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"]
        )
        configuration = RTCConfiguration(iceServers=[ice_server])
        self.pc = RTCPeerConnection(configuration=configuration)

        # self.pc.addTrack()

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("open")
            def on_open():
                print("data channel opened")

        @self.pc.on("negotiationneeded")
        def on_negotiationneeded(event):
            print("negotiation needed")

        self.accept()
        self.send(text_data=json.dumps({"text": "you are connected to ws 2"}))

    def receive(self, text_data=None, bytes_data=None):
        r = async_to_sync(self.Areceive)(text_data=text_data)
        if r:
            self.send(
                text_data=json.dumps(
                    {
                        "description": {
                            "sdp": r[0],
                            "type": r[1],
                        }
                    }
                )
            )

    async def Areceive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # local_video = CustomVideoTrack(1)
        # self.pc.addTrack(local_video)

        if "finalDes" in data:
            offer = RTCSessionDescription(
                sdp=data["finalDes"]["sdp"], type=data["finalDes"]["type"]
            )
            await self.pc.setRemoteDescription(offer)
            if self.pc.setRemoteDescription:
                answer = await self.pc.createAnswer()
                await self.pc.setLocalDescription(answer)
                r = [self.pc.localDescription.sdp, self.pc.localDescription.type]
                return r
