from rest_framework import serializers

from rides.models.ride_event import RideEvent

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'
