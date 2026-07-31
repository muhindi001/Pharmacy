from rest_framework import serializers
from .models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):

    status = serializers.BooleanField(
        required=False,
        default=True,
        allow_null=True,
    )
    medicines_count = serializers.IntegerField(
        read_only=True,
    )

    def to_internal_value(self, data):
        if isinstance(data, dict) and "status" in data:
            value = data.get("status")
            if isinstance(value, str):
                normalized = value.strip().lower()
                if normalized in {"true", "1", "yes", "y", "active", "enabled", "on"}:
                    data = data.copy()
                    data["status"] = True
                elif normalized in {"false", "0", "no", "n", "inactive", "disabled", "off"}:
                    data = data.copy()
                    data["status"] = False

        return super().to_internal_value(data)

    class Meta:
        model = Manufacturer
        fields = "__all__"