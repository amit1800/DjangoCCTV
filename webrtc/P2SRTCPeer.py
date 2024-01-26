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

from webrtc import customVideoTrack
from aiortc import (
    MediaStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    RTCConfiguration,
    RTCIceServer,
)
from aiortc.contrib.media import MediaRelay


class P2SRTCPeer:
    def __init__(self) -> None:
        pass

    async def handle(self, request, video, closeEvent):
        self.params = request
        # self.onClose = function
        self.video = video
        offer = RTCSessionDescription(sdp=self.params["sdp"], type=self.params["type"])
        ice_server = RTCIceServer(
            urls=["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"]
        )
        configuration = RTCConfiguration(iceServers=[ice_server])

        pc = RTCPeerConnection(configuration=configuration)
        transceiver = pc.addTransceiver(trackOrKind="video", direction="sendrecv")
        # local_video = customVideoTrack.CustomVideoTrack(self.params["framerate"])
        transceiver.sender.replaceTrack(self.video)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            if pc.iceConnectionState == "failed":
                # self.onClose(self)
                # print("connection failed")
                pass

        @pc.on("datachannel")
        def on_datachannel(channel):
            # to send periodic pings
            # async def send_pings():
            #     while True:
            #         msg = "ping"
            #         channel.send(msg)
            #         await asyncio.sleep(1)

            # asyncio.ensure_future(send_pings())

            print("data channel opened")
            channel.send("data channel opened")

            @channel.on("message")
            def on_message(m):
                print("data channel: " + m)

            @channel.on("close")
            def on_close():
                print("peer data channel closed")
                closeEvent()
                pc.close()

        @pc.on("track")
        def on_track(track):
            pass
            # pc.addTrack(track)
            # local_video = rtspOut("rtsp://192.168.214.72:1935")
            # local_video = rtspOut(track)
            # local_video = pureRtspOut(useDefaultFrameRate=False, framerate=15)
            # local_video = customVideoTrack.CustomVideoTrack(1)
            # pc.addTrack(local_video)

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        start_time = time.time()
        await pc.setLocalDescription(answer)
        print("--- %s seconds ---" % (time.time() - start_time))

        return HttpResponse(
            json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )
