from rest_framework import serializers

from .models import (
    Warehouse,
    WarehouseTransfer,
    WarehouseTransferItem,
)


class WarehouseSerializer(serializers.ModelSerializer):

    warehouse_type = serializers.ChoiceField(
        choices=Warehouse.WAREHOUSE_TYPES,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    type = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )
    inventory_count = serializers.IntegerField(
        read_only=True,
    )

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()

            if "warehouse_type" not in data and "type" in data:
                data["warehouse_type"] = data["type"]

            if "warehouse_type" not in data:
                data["warehouse_type"] = "MAIN"

        return super().to_internal_value(data)

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