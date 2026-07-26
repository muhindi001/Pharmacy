from rest_framework import serializers

from .models import PurchaseReturn, PurchaseReturnItem


class PurchaseReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseReturnItem
        fields = "__all__"


class PurchaseReturnSerializer(serializers.ModelSerializer):

    items = PurchaseReturnItemSerializer(many=True)

    class Meta:
        model = PurchaseReturn
        fields = "__all__"

    def create(self, validated_data):

        items = validated_data.pop("items")

        purchase_return = PurchaseReturn.objects.create(
            **validated_data
        )

        total = 0

        for item in items:

            purchase_item = item["purchase_item"]

            line_total = (
                item["quantity"] *
                item["unit_cost"]
            )

            PurchaseReturnItem.objects.create(
                purchase_return=purchase_return,
                total=line_total,
                **item,
            )

            total += line_total

        purchase_return.total_amount = total
        purchase_return.save()

        return purchase_return