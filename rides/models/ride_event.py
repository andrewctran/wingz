from django.db import models

from rides.models.ride import Ride


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, related_name="events", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
