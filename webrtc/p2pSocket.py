from django.shortcuts import render
from django.http import HttpResponse
from aiortc import rtcpeerconnection, rtcdatachannel
from django.shortcuts import render
import json


# Create your views here.
def p2pSocketIndex(req):
    return render(req, "./p2pSocket.html")
