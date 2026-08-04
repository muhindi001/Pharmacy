import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):

    transaction_number = django_filters.CharFilter(
        field_name="transaction_number",
        lookup_expr="icontains",
    )

    reference_number = django_filters.CharFilter(
        field_name="reference_number",
        lookup_expr="icontains",
    )

    customer = django_filters.UUIDFilter(
        field_name="customer",
    )

    cashier = django_filters.UUIDFilter(
        field_name="cashier",
    )

    sale = django_filters.UUIDFilter(
        field_name="sale",
    )

    payment = django_filters.UUIDFilter(
        field_name="payment",
    )

    transaction_type = django_filters.CharFilter(
        field_name="transaction_type",
        lookup_expr="iexact",
    )

    payment_method = django_filters.CharFilter(
        field_name="payment_method",
        lookup_expr="iexact",
    )

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    min_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="gte",
    )

    max_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="lte",
    )

    start_date = django_filters.DateFilter(
        field_name="transaction_date",
        lookup_expr="date__gte",
    )

    end_date = django_filters.DateFilter(
        field_name="transaction_date",
        lookup_expr="date__lte",
    )

    class Meta:
        model = Transaction

        fields = [
            "transaction_number",
            "reference_number",
            "customer",
            "cashier",
            "sale",
            "payment",
            "transaction_type",
            "payment_method",
            "status",
            "min_amount",
            "max_amount",
            "start_date",
            "end_date",
        ]