from rest_framework import serializers

from rides.models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "role",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )
