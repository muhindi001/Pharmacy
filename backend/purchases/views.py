from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Purchase, PurchaseItem
from .serializers import PurchaseSerializer, PurchaseItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import receive_purchase


class PurchaseViewSet(viewsets.ModelViewSet):

    queryset = (
        Purchase.objects.select_related(
            "supplier",
            "created_by",
        )
        .prefetch_related(
            "items",
        )
    )

    serializer_class = PurchaseSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "purchase_number",
        "invoice_number",
        "supplier__supplier_name",
        "items__medicine__medicine_name",
        "items__batch_number",
    ]

    filterset_fields = [
        "status",
        "payment_status",
        "supplier",
        "purchase_date",
        "received_date",
    ]

    ordering_fields = [
        "purchase_date",
        "created_at",
        "total",
        "purchase_number",
    ]

    ordering = [
        "-purchase_date",
    ]

    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        purchase = self.get_object()

        receive_purchase(purchase, request=request)

        serializer = self.get_serializer(purchase)

        return Response(serializer.data)


class PurchaseItemViewSet(viewsets.ModelViewSet):

    queryset = (
        PurchaseItem.objects.select_related(
            "purchase",
            "medicine",
        )
    )

    serializer_class = PurchaseItemSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "medicine__medicine_name",
        "batch_number",
    ]

    filterset_fields = [
        "medicine",
        "expiry_date",
        "purchase",
    ]

    ordering_fields = [
        "expiry_date",
        "quantity",
        "unit_cost",
        "selling_price",
    ]

    ordering = [
        "expiry_date",
    ]