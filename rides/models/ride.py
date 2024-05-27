from django.db import models
from rides.models.user import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    rider = models.ForeignKey(User, related_name='rides_as_rider', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='rides_as_driver', on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
