from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .models import InventoryTransaction,Inventory
from .serializers import InventoryTransactionSerializer
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

class InventoryTransactionViewSet(viewsets.ModelViewSet):

    serializer_class = InventoryTransactionSerializer

    queryset = InventoryTransaction.objects.filter(
        is_deleted=False
    ).select_related(
        "medicine",
        "batch",
        "performed_by",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "medicine__medicine_name",
        "batch__batch_number",
        "reference_number",
    ]

    filterset_fields = [
        "transaction_type",
        "medicine",
        "batch",
        "performed_by",
    ]

    ordering_fields = [
        "transaction_date",
        "quantity",
        "created_at",
    ]

    ordering = [
        "-transaction_date",
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(
                transaction_date__date__range=[start_date, end_date]
            )

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()