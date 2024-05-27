from django.test import TestCase

from rides.models import User


class UserModelTestCase(TestCase):
    def test_user_creation(self):
        User.objects.create(
            role="admin",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="123456789",
        )
        user = User.objects.get(email="john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.phone_number, "123456789")
