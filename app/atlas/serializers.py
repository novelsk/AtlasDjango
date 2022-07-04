from rest_framework import serializers
from .models import SensorData


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ('ai_max', 'ai_min', 'ai_mean', 'stat_min', 'stat_max', 'ml_min', 'ml_max', 'mode', 'date')
