from rest_framework import serializers

from .models import GoodsReceipt
from .models import GoodsReceiptItem


class GoodsReceiptItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True
    )

    class Meta:
        model = GoodsReceiptItem

        fields = "__all__"


class GoodsReceiptSerializer(serializers.ModelSerializer):

    items = GoodsReceiptItemSerializer(
        many=True
    )

    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True
    )

    warehouse_name = serializers.CharField(
        source="warehouse.warehouse_name",
        read_only=True
    )

    class Meta:
        model = GoodsReceipt

        fields = "__all__"

    def create(self, validated_data):

        items = validated_data.pop("items")

        receipt = GoodsReceipt.objects.create(
            **validated_data
        )

        for item in items:
            GoodsReceiptItem.objects.create(
                receipt=receipt,
                **item
            )

        return receipt

    def update(self, instance, validated_data):

        validated_data.pop("items", None)

        return super().update(instance, validated_data)