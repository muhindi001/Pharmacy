from datetime import date, timedelta

from rest_framework import serializers

from categories.models import Category
from manufacturers.models import Manufacturer

from .models import Medicine


class CategoryFKField(serializers.Field):
    def to_internal_value(self, data):
        if data in (None, "", "null"):
            return Category.objects.order_by("id").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )

        try:
            return Category.objects.get(pk=data)
        except (Category.DoesNotExist, TypeError, ValueError):
            if isinstance(data, str):
                match = Category.objects.filter(category_name__iexact=data).first()
                if match:
                    return match
            return Category.objects.filter(category_name="General").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )

    def to_representation(self, value):
        if value is None:
            return None
        return value.pk


class ManufacturerFKField(serializers.Field):
    def to_internal_value(self, data):
        if data in (None, "", "null"):
            return None

        try:
            return Manufacturer.objects.get(pk=data)
        except (Manufacturer.DoesNotExist, TypeError, ValueError):
            if isinstance(data, str):
                match = Manufacturer.objects.filter(manufacturer_name__iexact=data).first()
                if match:
                    return match
            return None

    def to_representation(self, value):
        if value is None:
            return None
        return value.pk


class MedicineSerializer(serializers.ModelSerializer):
    generic_name = serializers.CharField(required=False, allow_blank=True)
    buying_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
    )
    expiry_date = serializers.DateField(required=False, allow_null=True)
    category = CategoryFKField(required=False, allow_null=True)
    manufacturer = ManufacturerFKField(required=False, allow_null=True)
    category_name = serializers.CharField(
        source="category.category_name",
        read_only=True,
    )
    status = serializers.CharField(required=False, allow_blank=True, write_only=True)
    purchase_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=0,
    )
    sku = serializers.CharField(required=False, allow_blank=True, write_only=True)
    supplier = serializers.IntegerField(required=False, write_only=True)
    tax_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        min_value=0,
        max_value=100,
    )

    def _resolve_category(self, value):
        if value in (None, "", "null"):
            return Category.objects.order_by("id").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )

        try:
            return Category.objects.get(pk=value)
        except (Category.DoesNotExist, TypeError, ValueError):
            if isinstance(value, str):
                match = Category.objects.filter(category_name__iexact=value).first()
                if match:
                    return match
            return Category.objects.filter(category_name="General").first() or Category.objects.create(
                category_name="General",
                description="Auto-created default category",
            )

    def _resolve_manufacturer(self, value):
        if value in (None, "", "null"):
            return None

        try:
            return Manufacturer.objects.get(pk=value)
        except (Manufacturer.DoesNotExist, TypeError, ValueError):
            if isinstance(value, str):
                match = Manufacturer.objects.filter(manufacturer_name__iexact=value).first()
                if match:
                    return match
            return None

    def validate(self, attrs):
        attrs = attrs.copy()

        attrs["category"] = self._resolve_category(attrs.get("category"))
        attrs["manufacturer"] = self._resolve_manufacturer(attrs.get("manufacturer"))

        if not attrs.get("generic_name"):
            attrs["generic_name"] = attrs.get("medicine_name", "") or "N/A"

        if "buying_price" not in attrs and "purchase_price" in attrs:
            attrs["buying_price"] = attrs["purchase_price"]

        if not attrs.get("buying_price"):
            attrs["buying_price"] = 0

        status_value = attrs.pop("status", None)
        if status_value is not None:
            attrs["is_active"] = str(status_value).strip().lower() in {
                "active",
                "true",
                "1",
                "yes",
                "y",
                "enabled",
                "open",
            }

        attrs.pop("purchase_price", None)
        attrs.pop("sku", None)
        attrs.pop("supplier", None)
        attrs.pop("tax_percentage", None)

        if not attrs.get("qty"):
            attrs["qty"] = 0

        if not attrs.get("expiry_date"):
            attrs["expiry_date"] = date.today() + timedelta(days=365)

        return attrs

    class Meta:
        model = Medicine

        fields = [
            "id",
            "medicine_name",
            "generic_name",
            "buying_price",
            "selling_price",
            "category",
            "category_name",
            "unit",
            "qty",
            "expiry_date",
            "is_active",
            "created_at",
            "updated_at",
            "manufacturer",
            "status",
            "purchase_price",
            "sku",
            "supplier",
            "tax_percentage",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )