from rest_framework import serializers

from .models import (
    Warehouse,
    WarehouseTransfer,
    WarehouseTransferItem,
)


class WarehouseSerializer(serializers.ModelSerializer):

    inventory_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Warehouse
        fields = "__all__"


class WarehouseTransferItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True
    )

    class Meta:
        model = WarehouseTransferItem
        fields = "__all__"


class WarehouseTransferSerializer(serializers.ModelSerializer):

    from_warehouse_name = serializers.CharField(
        source="from_warehouse.warehouse_name",
        read_only=True
    )

    to_warehouse_name = serializers.CharField(
        source="to_warehouse.warehouse_name",
        read_only=True
    )

    items = WarehouseTransferItemSerializer(
        many=True,
        read_only=True
    )

    total_items = serializers.SerializerMethodField()

    class Meta:
        model = WarehouseTransfer
        fields = "__all__"

    def get_total_items(self, obj):
        return obj.items.count()