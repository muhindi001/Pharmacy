from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import SalesReturn, SalesReturnItem
from .serializers import (
    SalesReturnSerializer,
    SalesReturnItemSerializer,
)


class SalesReturnViewSet(viewsets.ModelViewSet):

    serializer_class = SalesReturnSerializer

    queryset = SalesReturn.objects.select_related(
        "sale",
        "customer",
        "approved_by",
    ).prefetch_related(
        "items",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "return_number",
        "sale__sale_number",
    ]

    filterset_fields = [
        "status",
        "return_type",
    ]

    ordering = [
        "-return_date",
    ]


class SalesReturnItemViewSet(viewsets.ModelViewSet):

    serializer_class = SalesReturnItemSerializer

    queryset = SalesReturnItem.objects.select_related(
        "medicine",
        "batch",
        "sale_item",
    )