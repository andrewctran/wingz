import random
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from rides.models.ride import Ride
from rides.models.ride_event import RideEvent
from rides.models.user import User
from rides.serializers.ride_serializer import RideSerializer


class RideViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            phone_number="1234567890",
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
        )
        self.ride1 = Ride.objects.create(
            rider=self.user,
            driver=self.admin_user,
            pickup_latitude=40.7128,
            pickup_longitude=-74.0060,  # New York
            dropoff_latitude=random.uniform(-90, 0),
            dropoff_longitude=random.uniform(-180, 180),
            pickup_time=timezone.now(),
            status="en-route",
        )
        self.ride2 = Ride.objects.create(
            rider=self.user,
            driver=self.admin_user,
            pickup_latitude=34.0522,
            pickup_longitude=-118.2437,  # Los Angeles
            dropoff_latitude=random.uniform(-90, 0),
            dropoff_longitude=random.uniform(-180, 180),
            pickup_time=timezone.now() + timedelta(days=3),
            status="dropoff",
        )
        self.ride3 = Ride.objects.create(
            rider=self.user,
            driver=self.admin_user,
            pickup_latitude=41.8781,
            pickup_longitude=87.6298,  # Chicago
            dropoff_latitude=random.uniform(-90, 0),
            dropoff_longitude=random.uniform(-180, 180),
            pickup_time=timezone.now() + timedelta(hours=1),
            status="en-route",
        )
        with freeze_time(timezone.now() - timedelta(hours=2)):
            self.ride_event1 = RideEvent.objects.create(
                ride=self.ride1, description="foo",
            )
        with freeze_time(timezone.now() - timedelta(days=2)):
            self.ride_event2 = RideEvent.objects.create(
                ride=self.ride2, description="bar",
            )
        with freeze_time(timezone.now() - timedelta(hours=2)):
            self.ride_event3 = RideEvent.objects.create(
                ride=self.ride3, description="baz",
            )

    def test_admin_can_list_rides(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("ride-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_list_rides(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("ride-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_rides_by_status(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("ride-list"), {"status": "en-route"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_rides_by_rider_email(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(
            reverse("ride-list"), {"rider__email": "testuser@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_sort_rides_by_pickup_time(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("ride-list"), {"ordering": "pickup_time"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data["results"][0]["pickup_time"]
            < response.data["results"][1]["pickup_time"]
        )

    def test_sort_rides_by_distance(self):
        self.client.force_login(self.admin_user)

        gps_position = "40.730610,-73.935242"  # A point near New York

        url = f"{reverse('ride-list')}?gps_position={gps_position}&ordering=distance"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        ride_ids = [ride["id"] for ride in response_data["results"]]

        # ride1 and ride3 should come before ride2 since it is closer to the given GPS position
        self.assertEqual(ride_ids, [self.ride1.id, self.ride3.id, self.ride2.id])

    def test_todays_ride_events(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("ride-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for ride in response.data["results"]:
            # ride1 and ride3 should have associated ride events because those ride events took place in the past 24 hours
            if ride["id"] == self.ride1.id or ride["id"] == self.ride3.id:
                self.assertEqual(len(ride["todays_ride_events"]), 1)
            else:
                self.assertEqual(len(ride["todays_ride_events"]), 0)

    def test_pagination(self):
        self.client.force_login(self.admin_user)

        page_size = 2
        page_number = 1
        url = f"{reverse('ride-list')}?page_size={page_size}&page={page_number}"
        first_page_response = self.client.get(url)

        self.assertEqual(first_page_response.status_code, status.HTTP_200_OK)

        expected_first_page_rides = [
            self.ride1,
            self.ride3,
        ]  # Get expected rides for the first page
        first_page_serializer = RideSerializer(expected_first_page_rides, many=True)
        self.assertEqual(
            first_page_response.data["results"], first_page_serializer.data
        )
        self.assertEqual(first_page_response.data["count"], 3)
        self.assertEqual(len(first_page_response.data["results"]), page_size)

        next_page_response = self.client.get(first_page_response.data["next"])

        self.assertEqual(next_page_response.status_code, status.HTTP_200_OK)
        expected_next_page_rides = [self.ride2]  # Get expected rides for the next page
        next_page_serializer = RideSerializer(expected_next_page_rides, many=True)
        self.assertEqual(next_page_response.data["results"], next_page_serializer.data)
        self.assertEqual(next_page_response.data["count"], 3)
        self.assertEqual(len(next_page_response.data["results"]), 1)
