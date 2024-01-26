from django.shortcuts import render
from django.http import HttpResponse
from aiortc import rtcpeerconnection, rtcdatachannel
from django.shortcuts import render
import json


# Create your views here.
def getOffer(req):
    return HttpResponse(json.dumps({"offer": offer}))


def getAnswer(req):
    return HttpResponse(json.dumps({"answer": answer}))


def p2pHttpIndex(req):
    return render(req, "./p2pHttp.html")


def setOffer(req):
    data = json.loads(req.body)
    global offer
    offer = data
    print(data["type"])
    return HttpResponse(json.dumps({"message": "got the offer"}))


def setAnswer(req):
    data = json.loads(req.body)
    global answer
    answer = data
    print(data["type"])
    return HttpResponse(json.dumps({"message": "got the answer"}))
