from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .models import Sale, SaleItem
from .serializers import SaleSerializer, SaleItemSerializer


class SaleViewSet(viewsets.ModelViewSet):

    serializer_class = SaleSerializer

    queryset = Sale.objects.select_related(
        "customer",
        "cashier",
        "prescription",
    ).prefetch_related(
        "items",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "sale_number",
        "invoice_number",
        "receipt_number",
        "reference_number",
        "customer__customer_code",
        "customer__first_name",
        "customer__last_name",
        "cashier__username",
    ]

    filterset_fields = [
        "sale_type",
        "status",
        "cashier",
        "customer",
    ]

    ordering_fields = [
        "created_at",
        "total",
        "subtotal",
        "sale_number",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(
                created_at__date__range=[start_date, end_date]
            )

        return queryset

    def destroy(self, request, *args, **kwargs):

        sale = self.get_object()

        if sale.status == "Completed":
            return Response(
                {
                    "detail": "Completed sales cannot be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        sale.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class SaleItemViewSet(viewsets.ModelViewSet):

    serializer_class = SaleItemSerializer

    queryset = SaleItem.objects.select_related(
        "sale",
        "medicine",
        "batch",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "sale__sale_number",
        "medicine__medicine_name",
        "batch__batch_number",
    ]

    filterset_fields = [
        "medicine",
        "batch",
        "sale",
    ]

    ordering_fields = [
        "quantity",
        "unit_price",
        "total",
    ]