import django_filters

from sales.models import Sale


class CustomerSaleHistoryFilter(django_filters.FilterSet):

    sale_date_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte"
    )

    sale_date_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte"
    )

    invoice_number = django_filters.CharFilter(
        field_name="invoice_number",
        lookup_expr="icontains"
    )

    class Meta:
        model = Sale
        fields = ["status"]