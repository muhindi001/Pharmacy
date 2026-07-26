from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):

    serializer_class = SupplierSerializer

    queryset = Supplier.objects.filter(
        is_deleted=False
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "supplier_name",
        "company_name",
        "contact_person",
        "phone_number",
        "email",
    ]

    filterset_fields = [
        "payment_terms",
        "is_active",
    ]

    ordering_fields = [
        "supplier_name",
        "company_name",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "supplier_name",
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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()