from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from rides.models.user import User
from rides.serializers.user_serializer import UserSerializer


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.non_admin_user = User.objects.create(
            username="non_admin_user", email="non_admin_user@example.com"
        )

    def test_admin_can_access_user_list(self):
        self.client.force_login(self.admin_user)
        url = reverse("user-list")
        response = self.client.get(url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_non_admin_cannot_access_user_list(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_user_detail(self):
        self.client.force_login(self.admin_user)
        url = reverse("user-detail", args=[self.non_admin_user.pk])
        response = self.client.get(url)
        user = User.objects.get(pk=self.non_admin_user.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_non_admin_cannot_access_user_detail(self):
        self.client.force_login(self.non_admin_user)
        url = reverse("user-detail", args=[self.non_admin_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user(self):
        self.client.force_login(self.admin_user)
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "1234567890",
            "role": "foo",
        }
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_non_admin_cannot_create_user(self):
        self.client.force_login(self.non_admin_user)
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "1234567890",
            "role": "foo",
        }
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)

    def test_admin_can_update_user(self):
        self.client.force_login(self.admin_user)
        data = {
            "username": "non_admin_user",
            "email": "updateduser@example.com",
            "password": "updatedpass",
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "1234567890",
            "role": "foo",
        }
        response = self.client.put(
            reverse("user-detail", args=[self.non_admin_user.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.non_admin_user.refresh_from_db()
        self.assertEqual(self.non_admin_user.email, "updateduser@example.com")

    def test_non_admin_cannot_update_user(self):
        self.client.force_login(self.non_admin_user)
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": "updatedpass",
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "1234567890",
            "role": "foo",
        }
        response = self.client.put(
            reverse("user-detail", args=[self.non_admin_user.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
