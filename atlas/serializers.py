from rest_framework import serializers
from .models import Cmn, Ai


class CmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cmn


class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai
