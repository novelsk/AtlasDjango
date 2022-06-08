from rest_framework import serializers
from .models import Cmn, Ai, AtlasUser


class CmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cmn
        fields = '__all__'


class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai
        fields = '__all__'


class UserGroups(serializers.ModelSerializer):
    class Meta:
        model = AtlasUser
        fields = ['objects_cmn_groups', 'objects_ai_groups']
