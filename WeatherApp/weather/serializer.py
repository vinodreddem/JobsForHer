from rest_framework import serializers
from . import models

class WeatherSerializers (serializers.ModelSerializer):
    class Meta:
        model = models.WeatherData
        fields = '__all__'
