from django.test import TestCase
from rides.models import User
from rides.serializers import UserSerializer

class UserSerializerTestCase(TestCase):
    def test_user_serializer(self):
        data = {
            'role': 'admin',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '123456789'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.role, 'admin')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.phone_number, '123456789')