from rest_framework import serializers
from .models import ObjectEvent


class ObjectEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectEvent
        fields = '__all__'
