from django.db.models import Prefetch
from django.utils import timezone
from django.utils.timezone import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import geodesic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from rides.models.ride import Ride
from rides.models.ride_event import RideEvent
from rides.serializers.ride_serializer import RideSerializer


class RidePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    pagination_class = RidePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "rider__email"]
    ordering_fields = ["pickup_time"]
    ordering = ["pickup_time"]
    queryset = Ride.objects.all()

    def get_queryset(self):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        prefetch = Prefetch(
            "events",
            queryset=RideEvent.objects.filter(created_at__gte=last_24_hours),
            to_attr="todays_ride_events",
        )

        return (
            Ride.objects.select_related("rider", "driver")
            .prefetch_related(prefetch)
            .all()
        )

    @action(detail=False, methods=["get"])
    def distance_sort(self, request):
        gps_position = request.query_params.get("gps_position", None)
        if not gps_position:
            return Response({"error": "GPS position is required."}, status=400)

        try:
            gps_latitude, gps_longitude = map(float, gps_position.split(","))
        except ValueError:
            return Response({"error": "Invalid GPS position format."}, status=400)

        queryset = (
            self.get_queryset()
            .annotate(
                distance_from_gps_position=geodesic(
                    (gps_latitude, gps_longitude),
                    (ride.pickup_latitude, ride.pickup_longitude),
                ).km
            )
            .order_by("distance_from_gps_position")
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
