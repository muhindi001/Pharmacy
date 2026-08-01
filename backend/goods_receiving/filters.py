import django_filters

from .models import GoodsReceipt


class GoodsReceiptFilter(django_filters.FilterSet):

    received_from = django_filters.DateFilter(
        field_name="received_date",
        lookup_expr="gte",
    )

    received_to = django_filters.DateFilter(
        field_name="received_date",
        lookup_expr="lte",
    )

    class Meta:

        model = GoodsReceipt

        fields = [
            "status",
            "supplier",
            "warehouse",
        ]