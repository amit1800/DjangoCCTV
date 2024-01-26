from rest_framework import serializers
from base.models import CUser


class CUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        fields = "__all__"
