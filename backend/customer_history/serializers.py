from rest_framework import serializers

from sales.models import Sale
from sales.models import SaleItem


class SaleItemHistorySerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True
    )

    class Meta:
        model = SaleItem
        fields = (
            "id",
            "medicine_name",
            "quantity",
            "unit_price",
            "discount",
            "total",
        )


class CustomerSaleHistorySerializer(serializers.ModelSerializer):

    items = SaleItemHistorySerializer(
        many=True,
        read_only=True,
    )

    customer_name = serializers.SerializerMethodField()

    def get_customer_name(self, obj):
        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}".strip()
        return ""

    class Meta:
        model = Sale

        fields = (
            "id",
            "invoice_number",
            "created_at",
            "customer_name",
            "status",
            "subtotal",
            "discount",
            "tax",
            "total",
            "items",
        )