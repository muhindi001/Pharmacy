from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Inventory
from .serializers import InventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):

    queryset = Inventory.objects.select_related(
        "medicine",
        "batch",
    )

    serializer_class = InventorySerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "medicine__medicine_name",
        "medicine__generic_name",
        "batch__batch_number",
    ]

    filterset_fields = [
        "medicine",
    ]

    ordering_fields = [
        "quantity",
        "available_quantity",
        "last_updated",
    ]

    ordering = [
        "medicine__medicine_name",
    ]

