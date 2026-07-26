from rest_framework import serializers
from .models import Sale, SaleItem
from .services import process_sale

class SaleItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "medicine",
            "medicine_name",
            "batch",
            "quantity",
            "unit_price",
            "cost_price",
            "discount",
            "tax",
            "profit",
            "expiry_date",
            "total",
        ]
        read_only_fields = [
            "id",
        ]


class SaleSerializer(serializers.ModelSerializer):

    items = SaleItemSerializer(
        many=True,
    )

    customer_name = serializers.SerializerMethodField()

    cashier_name = serializers.SerializerMethodField()

    class Meta:
        model = Sale

        fields = [
            "id",
            "sale_number",
            "invoice_number",
            "receipt_number",
            "reference_number",
            "customer",
            "customer_name",
            "prescription",
            "cashier",
            "cashier_name",
            "sale_type",
            "subtotal",
            "discount",
            "tax",
            "total",
            "notes",
            "status",
            "created_at",
            "updated_at",
            "items",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_customer_name(self, obj):

        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"

        return None

    def get_cashier_name(self, obj):

        if obj.cashier:
            return obj.cashier.get_full_name() or obj.cashier.username

        return None

    def create(self, validated_data):

        items = validated_data.pop("items")

        return process_sale(
            validated_data,
            items,
        )

    def update(self, instance, validated_data):

        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if items_data is not None:

            instance.items.all().delete()

            for item in items_data:

                SaleItem.objects.create(
                    sale=instance,
                    **item,
                )

        return instance