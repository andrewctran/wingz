from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from rides.models.ride import Ride
from rides.serializers.ride_event_serializer import RideEventSerializer
from rides.serializers.user_serializer import UserSerializer


class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id",
            "rider",
            "driver",
            "pickup_time",
            "status",
            "todays_ride_events",
        ]

    def get_todays_ride_events(self, obj):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        todays_events = obj.events.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(todays_events, many=True).data
