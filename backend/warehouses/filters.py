import django_filters

from .models import (
    Warehouse,
    WarehouseTransfer,
)


class WarehouseFilter(django_filters.FilterSet):

    warehouse_name = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    code = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    warehouse_type = django_filters.CharFilter()

    status = django_filters.CharFilter()

    manager = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    created_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    created_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Warehouse

        fields = [
            "warehouse_name",
            "code",
            "warehouse_type",
            "status",
            "manager",
        ]


class WarehouseTransferFilter(django_filters.FilterSet):

    transfer_number = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    status = django_filters.CharFilter()

    from_warehouse = django_filters.NumberFilter(
        field_name="from_warehouse"
    )

    to_warehouse = django_filters.NumberFilter(
        field_name="to_warehouse"
    )

    transfer_from = django_filters.DateFilter(
        field_name="transfer_date",
        lookup_expr="gte",
    )

    transfer_to = django_filters.DateFilter(
        field_name="transfer_date",
        lookup_expr="lte",
    )

    class Meta:
        model = WarehouseTransfer

        fields = [
            "transfer_number",
            "status",
            "from_warehouse",
            "to_warehouse",
        ]