from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Prescription, PrescriptionItem
from .serializers import (
    PrescriptionSerializer,
    PrescriptionItemSerializer,
)


class PrescriptionViewSet(viewsets.ModelViewSet):

    serializer_class = PrescriptionSerializer

    queryset = Prescription.objects.select_related(
        "customer",
        "verified_by",
    ).prefetch_related(
        "items",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "prescription_number",
        "doctor_name",
        "doctor_license_number",
        "customer__first_name",
        "customer__last_name",
    ]

    filterset_fields = [
        "status",
        "customer",
    ]

    ordering_fields = [
        "date_issued",
        "expiry_date",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]


class PrescriptionItemViewSet(viewsets.ModelViewSet):

    serializer_class = PrescriptionItemSerializer

    queryset = PrescriptionItem.objects.select_related(
        "prescription",
        "medicine",
    )