from rest_framework import serializers

from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False, allow_blank=True)
    contact_person = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True, write_only=True)
    city = serializers.CharField(required=False, allow_blank=True, write_only=True)
    country = serializers.CharField(required=False, allow_blank=True, write_only=True)
    status = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        attrs = attrs.copy()

        if not attrs.get("company_name"):
            attrs["company_name"] = attrs.get("supplier_name", "") or "Unknown Company"

        if not attrs.get("contact_person"):
            attrs["contact_person"] = "N/A"

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

        attrs.pop("code", None)
        attrs.pop("city", None)
        attrs.pop("country", None)

        return attrs

    class Meta:
        model = Supplier

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )