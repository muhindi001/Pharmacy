from decimal import Decimal

from rest_framework import serializers

from .models import Purchase, PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    class Meta:
        model = PurchaseItem
        fields = "__all__"
        read_only_fields = ("purchase",)

    def validate(self, attrs):

        if attrs["quantity"] <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        if attrs["unit_cost"] <= 0:
            raise serializers.ValidationError(
                "Unit cost must be greater than zero."
            )

        if attrs["selling_price"] < attrs["unit_cost"]:
            raise serializers.ValidationError(
                "Selling price cannot be lower than unit cost."
            )

        return attrs


class PurchaseSerializer(serializers.ModelSerializer):

    items = PurchaseItemSerializer(many=True)

    supplier_name = serializers.CharField(
        source="supplier.supplier_name",
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = (
            "purchase_number",
            "subtotal",
            "total",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):

        items_data = validated_data.pop("items")

        subtotal = Decimal("0.00")
        total_tax = Decimal("0.00")
        total_discount = Decimal("0.00")

        purchase = Purchase.objects.create(**validated_data)

        for item in items_data:

            quantity = item["quantity"]
            unit_cost = item["unit_cost"]
            tax = item.get("tax", Decimal("0.00"))
            discount = item.get("discount", Decimal("0.00"))

            line_total = (
                quantity * unit_cost
            ) + tax - discount

            PurchaseItem.objects.create(
                purchase=purchase,
                total=line_total,
                **item,
            )

            subtotal += quantity * unit_cost
            total_tax += tax
            total_discount += discount

        purchase.subtotal = subtotal
        purchase.tax = total_tax
        purchase.discount = total_discount
        purchase.total = (
            subtotal + total_tax - total_discount
        )

        purchase.save()

        return purchase

    def update(self, instance, validated_data):

        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if items_data is not None:

            instance.items.all().delete()

            subtotal = Decimal("0.00")
            total_tax = Decimal("0.00")
            total_discount = Decimal("0.00")

            for item in items_data:

                quantity = item["quantity"]
                unit_cost = item["unit_cost"]
                tax = item.get("tax", Decimal("0.00"))
                discount = item.get("discount", Decimal("0.00"))

                line_total = (
                    quantity * unit_cost
                ) + tax - discount

                PurchaseItem.objects.create(
                    purchase=instance,
                    total=line_total,
                    **item,
                )

                subtotal += quantity * unit_cost
                total_tax += tax
                total_discount += discount

            instance.subtotal = subtotal
            instance.tax = total_tax
            instance.discount = total_discount
            instance.total = (
                subtotal + total_tax - total_discount
            )

            instance.save()

        return instance