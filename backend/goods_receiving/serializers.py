from rest_framework import serializers

from medicines.models import Medicine
from .models import GoodsReceipt
from .models import GoodsReceiptItem


class GoodsReceiptItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True
    )

    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), required=False, allow_null=True)

    class Meta:
        model = GoodsReceiptItem
        fields = [
            "id",
            "medicine",
            "medicine_name",
            "batch_number",
            "manufacturing_date",
            "expiry_date",
            "ordered_quantity",
            "received_quantity",
            "accepted_quantity",
            "rejected_quantity",
            "purchase_price",
            "selling_price",
            "shelf_location",
            "inventory_updated",
        ]


class GoodsReceiptSerializer(serializers.ModelSerializer):

    items = GoodsReceiptItemSerializer(many=True, required=False)

    supplier_name = serializers.CharField(source="supplier.supplier_name", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.warehouse_name", read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = [
            "id",
            "grn_number",
            "purchase",
            "supplier",
            "supplier_name",
            "warehouse",
            "warehouse_name",
            "invoice_number",
            "delivery_note",
            "received_date",
            "received_by",
            "remarks",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        receipt = GoodsReceipt.objects.create(**validated_data)

        for item in items:
            GoodsReceiptItem.objects.create(receipt=receipt, **item)

        return receipt

    def update(self, instance, validated_data):
        validated_data.pop("items", None)
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()
            if "items" in data and isinstance(data["items"], list):
                normalized_items = []
                for item in data["items"]:
                    if isinstance(item, dict):
                        normalized_item = dict(item)
                        medicine = normalized_item.get("medicine")
                        if isinstance(medicine, str) and medicine:
                            try:
                                normalized_item["medicine"] = Medicine.objects.get(id=medicine)
                            except Medicine.DoesNotExist:
                                pass
                        normalized_items.append(normalized_item)
                    else:
                        normalized_items.append(item)
                data["items"] = normalized_items
        return super().to_internal_value(data)