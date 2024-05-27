import random

from django.test import TestCase
from django.utils import timezone

from rides.models.user import User
from rides.serializers.ride_serializer import RideSerializer
from rides.serializers.user_serializer import UserSerializer


class RideSerializerTestCase(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="driver@example.com",
            username="driver@example.com",
            phone_number="1234567890",
            role="user",
        )
        self.rider = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="rider@example.com",
            username="rider@example.com",
            phone_number="0987654321",
            role="user",
        )

    def test_ride_serializer(self):
        data = {
            "status": "en-route",
            "rider": UserSerializer(self.rider).data,
            "driver": UserSerializer(self.driver).data,
            "pickup_latitude": random.uniform(-90, 0),
            "pickup_longitude": random.uniform(-180, 180),
            "dropoff_latitude": random.uniform(-90, 0),
            "dropoff_longitude": random.uniform(-180, 180),
            "pickup_time": timezone.now(),
        }
        serializer = RideSerializer(data=data)
        self.assertTrue(serializer.is_valid())
