from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import StockAlert
from .serializers import StockAlertSerializer


class StockAlertViewSet(viewsets.ModelViewSet):

    serializer_class = StockAlertSerializer

    queryset = StockAlert.objects.select_related(
        "medicine",
        "batch",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "medicine__medicine_name",
        "batch__batch_number",
        "message",
    ]

    filterset_fields = [
        "alert_type",
        "status",
        "email_sent",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]