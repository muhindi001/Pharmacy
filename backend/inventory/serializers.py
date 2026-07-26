from rest_framework import serializers

from .models import InventoryTransaction,Inventory


class InventoryTransactionSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    class Meta:
        model = InventoryTransaction
        fields = "__all__"

        read_only_fields = (
            "id",
            "transaction_date",
            "created_at",
            "updated_at",
        )
class InventorySerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    class Meta:
        model = Inventory
        fields = "__all__"