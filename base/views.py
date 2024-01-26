from django.contrib.auth.hashers import check_password
from base.models import CUser


def isAuthenticated(username, password):
    if username is None or password is None or username == "" or password == "":
        return False
    try:
        if check_password(password, CUser.objects.get(username=username).password):
            print("****************USER EXISTS*********************")
            return True
        else:
            print("****************USER DOES NOT EXISTS*********************")
            return False
    except:
        return False
