from django.test import TestCase
from rides.models import Ride, User
from django.utils import timezone
from datetime import timedelta

class RideModelTestCase(TestCase):
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
            role="user"
        )

    def test_ride_creation(self):
        ride = Ride.objects.create(
            status="en-route",
            rider=self.rider,
            driver=self.driver,
            pickup_latitude=40.7128,
            pickup_longitude=-74.0060,
            dropoff_latitude=34.0522,
            dropoff_longitude=-118.2437,
            pickup_time=timezone.now() + timedelta(hours=1)
        )

        self.assertIsNotNone(ride)
        self.assertEqual(ride.status, "en-route")
        self.assertEqual(ride.rider, self.rider)
        self.assertEqual(ride.driver, self.driver)
        self.assertEqual(ride.pickup_latitude, 40.7128)
        self.assertEqual(ride.pickup_longitude, -74.0060)
        self.assertEqual(ride.dropoff_latitude, 34.0522)
        self.assertEqual(ride.dropoff_longitude, -118.2437)
        self.assertLess(timezone.now(), ride.pickup_time)
