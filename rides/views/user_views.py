from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from rides.models.user import User
from rides.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
