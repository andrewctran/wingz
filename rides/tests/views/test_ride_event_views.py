from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from rides.models import Ride, RideEvent, User


class RideEventViewSetTestCase(APITestCase):
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
        self.non_admin_user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
        )
        self.ride = Ride.objects.create(
            rider=self.non_admin_user,
            driver=self.admin_user,
            pickup_latitude=40.7128,
            pickup_longitude=-74.0060,
            dropoff_latitude=34.0522,
            dropoff_longitude=-118.2437,
            pickup_time=timezone.now(),
        )
        self.ride_event = RideEvent.objects.create(
            ride=self.ride, description="pickup",
        )

    def test_admin_can_list_ride_events(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("rideevent-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_list_ride_events(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.get(reverse("rideevent-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_ride_event(self):
        self.client.force_login(self.admin_user)
        data = {
            "ride": self.ride.id,
            "description": "dropoff",
        }
        response = self.client.post(reverse("rideevent-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideEvent.objects.count(), 2)

    def test_non_admin_cannot_create_ride_event(self):
        self.client.force_login(self.non_admin_user)
        data = {
            "ride": self.ride.id,
            "description": "dropoff",
        }
        response = self.client.post(reverse("rideevent-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(RideEvent.objects.count(), 1)

    def test_admin_can_retrieve_ride_event(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(
            reverse("rideevent-detail", args=[self.ride_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_retrieve_ride_event(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.get(
            reverse("rideevent-detail", args=[self.ride_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_ride_event(self):
        self.client.force_login(self.admin_user)
        data = {
            "ride": self.ride.id,
            "description": "en-route",
        }
        response = self.client.put(
            reverse("rideevent-detail", args=[self.ride_event.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride_event.refresh_from_db()
        self.assertEqual(self.ride_event.description, "en-route")

    def test_non_admin_cannot_update_ride_event(self):
        self.client.force_login(self.non_admin_user)
        data = {
            "ride": self.ride.id,
            "description": "en-route",
        }
        response = self.client.put(
            reverse("rideevent-detail", args=[self.ride_event.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_ride_event(self):
        self.client.force_login(self.admin_user)
        response = self.client.delete(
            reverse("rideevent-detail", args=[self.ride_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RideEvent.objects.count(), 0)

    def test_non_admin_cannot_delete_ride_event(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.delete(
            reverse("rideevent-detail", args=[self.ride_event.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(RideEvent.objects.count(), 1)
