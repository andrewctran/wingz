from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rides.views.ride_event_views import RideEventViewSet
from rides.views.ride_views import RideViewSet
from rides.views.user_views import UserViewSet

router = DefaultRouter()
router.register(r"rides", RideViewSet)
router.register(r"users", UserViewSet)
router.register(r"ride-events", RideEventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
