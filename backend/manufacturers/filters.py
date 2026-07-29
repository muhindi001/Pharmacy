import django_filters
from .models import Manufacturer


class ManufacturerFilter(
    django_filters.FilterSet
):

    manufacturer_name = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    country = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    status = django_filters.BooleanFilter()

    class Meta:
        model = Manufacturer

        fields = [
            "manufacturer_name",
            "country",
            "status",
        ]