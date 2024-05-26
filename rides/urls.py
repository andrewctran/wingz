from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, UserViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)
router.register(r'users', UserViewSet)
router.register(r'ride-events', RideEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]