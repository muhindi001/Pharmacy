import django_filters

from .models import AuditLog


class AuditLogFilter(django_filters.FilterSet):

    action = django_filters.CharFilter(
        field_name="action",
        lookup_expr="iexact",
    )

    module = django_filters.CharFilter(
        field_name="module",
        lookup_expr="icontains",
    )

    username = django_filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains",
    )

    ip_address = django_filters.CharFilter(
        field_name="ip_address",
        lookup_expr="icontains",
    )

    object_id = django_filters.CharFilter(
        field_name="object_id",
    )

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = AuditLog

        fields = [
            "action",
            "module",
            "username",
            "ip_address",
            "object_id",
        ]