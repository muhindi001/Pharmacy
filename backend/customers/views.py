from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerSerializer

    queryset = Customer.objects.filter(
        is_deleted=False
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "customer_code",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "loyalty_card_number",
    ]

    filterset_fields = [
        "status",
        "loyalty_tier",
    ]

    ordering_fields = [
        "customer_code",
        "first_name",
        "loyalty_points",
        "created_at",
    ]

    ordering = [
        "first_name",
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