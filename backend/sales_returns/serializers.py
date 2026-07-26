from rest_framework import serializers

from .models import SalesReturn, SalesReturnItem


class SalesReturnItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesReturnItem
        fields = "__all__"


class SalesReturnSerializer(serializers.ModelSerializer):

    items = SalesReturnItemSerializer(
        many=True,
    )

    class Meta:
        model = SalesReturn
        fields = "__all__"

    def create(self, validated_data):

        items = validated_data.pop("items")

        sales_return = SalesReturn.objects.create(
            **validated_data
        )

        for item in items:

            SalesReturnItem.objects.create(
                sales_return=sales_return,
                **item
            )

        return sales_return