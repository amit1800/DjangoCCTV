from django.http import HttpResponse
from webrtc.P2SRTCPeer import P2SRTCPeer
from webrtc.S2SRTCPeer import S2SRTCPeer
from aiortc.contrib.media import MediaRelay
from webrtc.faceDetectionTrack import FaceDetectionTrack
import uuid


class Pairing:
    id = 0
    free = True
    video = 0
    relay = MediaRelay()

    def __init__(self, s2sOffer, id=id) -> None:
        self.s2sOffer = s2sOffer
        self.pcon = P2SRTCPeer()
        self.scon = S2SRTCPeer()
        self.id = id
        self.uuid = uuid.uuid4()

    def closeEvent(self):
        # del self.pcon
        self.free = True
        print("peer closed, so pairing is open. free:", self.free)

    async def connectP2S(self, P2Srequest):
        if self.free:
            res = await self.pcon.handle(
                request=P2Srequest,
                video=self.relay.subscribe(track=self.video),
                closeEvent=self.closeEvent,
            )
            self.free = False
            return res
        else:
            return HttpResponse("not available")

    async def connectS2S(self):
        res = await self.scon.handle(offer=self.s2sOffer, uuid=self.uuid)
        self.video = self.scon.getS()
        return res
