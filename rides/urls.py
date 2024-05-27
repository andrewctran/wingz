from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rides.views.user_views import UserViewSet
from rides.views.ride_event_views import RideEventViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)
router.register(r'users', UserViewSet)
router.register(r'ride-events', RideEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]