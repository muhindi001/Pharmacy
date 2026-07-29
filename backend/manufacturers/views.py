from rest_framework import viewsets
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Manufacturer
from .serializers import ManufacturerSerializer
from .filters import ManufacturerFilter


class ManufacturerViewSet(viewsets.ModelViewSet):

    serializer_class = ManufacturerSerializer

    queryset = (
        Manufacturer.objects
        .annotate(
            medicines_count=Count("medicines")
        )
        .order_by("manufacturer_name")
    )
filter_backends = [DjangoFilterBackend]
filterset_class = ManufacturerFilter
search_fields = [
    "manufacturer_name",
    "code",
    "phone_number",
]