from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Transactions
    """
    filterset_class = TransactionFilter
    queryset = Transaction.objects.select_related(
        "sale",
        "payment",
        "customer",
        "cashier",
    )

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "transaction_type",
        "payment_method",
        "status",
        "cashier",
        "customer",
    ]
    filterset_fields = [
    "transaction_type",
    "payment_method",
    "status",
    "cashier",
    "customer",
]

    search_fields = [
        "transaction_number",
        "reference_number",
        "customer__customer_name",
    ]

    ordering_fields = [
        "transaction_date",
        "amount",
        "created_at",
    ]

    ordering = ["-transaction_date"]