from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from base.models import CUser

# Create your views here.


@api_view(["POST"])
def authenticate(request):
    us = request.data["username"]
    pw = request.data["password"]
    print(us, make_password(pw))

    # if CloudUser.objects.get(email = em).password ==pw:
    if check_password(pw, CUser.objects.get(username=us).password):
        print("****************USER EXISTS*********************")
        return Response({"auth": True})
    else:
        print("****************USER DOES NOT EXISTS*********************")
        return Response({"auth": False})
