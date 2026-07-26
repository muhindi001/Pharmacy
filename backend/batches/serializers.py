from rest_framework import serializers

from .models import Batch


class BatchSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True,
    )

    class Meta:
        model = Batch

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )