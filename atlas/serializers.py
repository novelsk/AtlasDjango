from rest_framework import serializers
from .models import Cmn, Ai


class CmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cmn
        fields = '__all__'


class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai
        fields = '__all__'
