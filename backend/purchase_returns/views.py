from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import PurchaseReturn, PurchaseReturnItem
from .serializers import (
    PurchaseReturnSerializer,
    PurchaseReturnItemSerializer,
)


class PurchaseReturnViewSet(viewsets.ModelViewSet):

    queryset = PurchaseReturn.objects.select_related(
        "purchase",
        "supplier",
        "approved_by",
    ).prefetch_related(
        "items",
    )

    serializer_class = PurchaseReturnSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "return_number",
        "purchase__purchase_number",
        "supplier__supplier_name",
    ]

    filterset_fields = [
        "status",
        "return_type",
        "supplier",
    ]

    ordering = [
        "-return_date",
    ]


class PurchaseReturnItemViewSet(viewsets.ModelViewSet):

    queryset = PurchaseReturnItem.objects.select_related(
        "medicine",
        "batch",
        "purchase_item",
    )

    serializer_class = PurchaseReturnItemSerializer