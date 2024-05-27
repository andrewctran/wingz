import random

from django.test import TestCase
from django.utils import timezone

from rides.models.ride import Ride
from rides.models.ride_event import RideEvent
from rides.models.user import User


class RideEventModelTestCase(TestCase):
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
            pickup_latitude=random.uniform(-90, 0),
            pickup_longitude=random.uniform(-180, 180),
            dropoff_latitude=random.uniform(-90, 0),
            dropoff_longitude=random.uniform(-180, 180),
            pickup_time=timezone.now(),
        )

    def test_ride_event_creation(self):
        ride_event = RideEvent.objects.create(
            ride=self.ride, description="Arrived at pickup location"
        )

        self.assertIsNotNone(ride_event)
        self.assertEqual(ride_event.ride, self.ride)
        self.assertEqual(ride_event.description, "Arrived at pickup location")
        self.assertIsNotNone(ride_event.created_at)
