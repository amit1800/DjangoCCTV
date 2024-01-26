import asyncio
import json
from av import VideoFrame
import logging
import time
from asgiref.sync import async_to_sync

# import cv2
import os
from django.http import HttpResponse


from django.shortcuts import render
import json
from base.views import isAuthenticated
from webrtc import customVideoTrack
from aiortc import (
    MediaStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    RTCConfiguration,
    RTCIceServer,
)
from aiortc.contrib.media import MediaRelay


class S2SRTCPeer:
    def __init__(self) -> None:
        self.video = None

    def getS(self):
        if self.video:
            return self.video
        else:
            return None

    # def object_from_string(self, message_str):
    #     try:
    #         message = json.loads(message_str)
    #         offer = json.loads(message["offer"])
    #         username = message["username"]
    #         password = message["password"]
    #         print("message:", username, password)
    #         if isAuthenticatedS2S(username, password):
    #             if offer["type"] in ["answer", "offer"]:
    #                 return RTCSessionDescription(**offer)
    #         else:
    #             return "auth failed"
    #     except:
    #         return "error"

    def object_to_string(self, obj):
        try:
            if isinstance(obj, RTCSessionDescription):
                message = {"sdp": obj.sdp, "type": obj.type}
            return json.dumps(message, sort_keys=True)
        except:
            return "error"

    async def handle(self, offer, uuid):
        self.uuid = uuid
        pc = RTCPeerConnection()
        transceiver = pc.addTransceiver(trackOrKind="video", direction="recvonly")
        transceiver.direction = "recvonly"

        # obj = self.object_from_string(request.body)
        obj = offer

        @pc.on("track")
        def on_track(remoteSteamTrack):
            self.video = remoteSteamTrack
            print("recieved video track", remoteSteamTrack.id)

        @pc.on("datachannel")
        def on_datachannel(channel):
            print("recieved a channel")

            @channel.on("message")
            def on_message(message):
                # print("<", message)
                pass

            @channel.on("close")
            def on_close():
                print("server data channel closed")
                pc.close()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            await pc.setLocalDescription(await pc.createAnswer())
            # print("local:", pc.localDescription, "remote:", pc.remoteDescription)
            return HttpResponse(self.object_to_string(pc.localDescription))
            # return web.Response(text=object_to_string(pc.localDescription))

        else:
            print(obj)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input)
        # return web.Response(text="bad req")
        return HttpResponse(json.loads('{"msg":"helo"}'))
