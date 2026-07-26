from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Batch
from .serializers import BatchSerializer


class BatchViewSet(viewsets.ModelViewSet):

    serializer_class = BatchSerializer

    queryset = Batch.objects.filter(
        is_deleted=False
    ).select_related(
        "medicine",
        "supplier",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "batch_number",
        "medicine__medicine_name",
        "medicine__generic_name",
        "supplier__supplier_name",
    ]

    filterset_fields = [
        "medicine",
        "supplier",
        "status",
        "purchase_date",
        "expiry_date",
    ]

    ordering_fields = [
        "purchase_date",
        "expiry_date",
        "quantity",
        "remaining_quantity",
        "purchase_price",
        "selling_price",
        "created_at",
    ]

    ordering = [
        "-purchase_date",
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(
                purchase_date__range=[start_date, end_date]
            )

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()