from django.urls import re_path
from . import consumers, webRtcConsumer

websocket_urlpatterns = [
    re_path(r"ws/socket-server/", consumers.P2PConsumer.as_asgi()),
    re_path(r"ws/server-to-peer/", webRtcConsumer.serverToPeerWS.as_asgi()),
]
