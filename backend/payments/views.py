from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer

    queryset = Payment.objects.select_related(
        "sale",
        "customer",
        "cashier",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "payment_number",
        "transaction_reference",
        "sale__sale_number",
        "customer__first_name",
        "customer__last_name",
    ]

    filterset_fields = [
        "payment_method",
        "status",
        "cashier",
    ]

    ordering_fields = [
        "payment_date",
        "amount",
    ]

    ordering = [
        "-payment_date",
    ]