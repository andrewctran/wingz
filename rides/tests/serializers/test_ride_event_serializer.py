from django.test import TestCase
from django.utils import timezone

from rides.models.ride import Ride
from rides.models.user import User
from rides.serializers.ride_event_serializer import RideEventSerializer


class RideEventSerializerTestCase(TestCase):
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

        self.ride = Ride.objects.create(
            status="en-route",
            rider=self.rider,
            driver=self.driver,
            pickup_latitude=40.7128,
            pickup_longitude=-74.0060,
            dropoff_latitude=34.0522,
            dropoff_longitude=-118.2437,
            pickup_time=timezone.now(),
        )

    def test_ride_event_serializer(self):
        data = {
            "ride": self.ride.id,
            "description": "Test event",
        }
        serializer = RideEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        ride_event = serializer.save()

        self.assertEqual(ride_event.description, "Test event")
