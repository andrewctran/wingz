from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from rides.models.ride_event import RideEvent
from rides.serializers.ride_event_serializer import RideEventSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
