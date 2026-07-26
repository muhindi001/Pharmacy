from rest_framework import serializers

from .models import Medicine


class MedicineSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.category_name",
        read_only=True,
    )

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
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )