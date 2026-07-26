from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Invoice, Receipt
from .serializers import InvoiceSerializer, ReceiptSerializer


class InvoiceViewSet(viewsets.ModelViewSet):

    serializer_class = InvoiceSerializer

    queryset = Invoice.objects.select_related(
        "sale",
        "customer",
        "payment",
    ).prefetch_related(
        "receipts",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "invoice_number",
        "sale__sale_number",
        "customer__first_name",
        "customer__last_name",
    ]

    filterset_fields = [
        "status",
    ]

    ordering_fields = [
        "invoice_date",
        "total",
    ]

    ordering = [
        "-invoice_date",
    ]


class ReceiptViewSet(viewsets.ModelViewSet):

    serializer_class = ReceiptSerializer

    queryset = Receipt.objects.select_related(
        "invoice",
        "payment",
        "cashier",
    )