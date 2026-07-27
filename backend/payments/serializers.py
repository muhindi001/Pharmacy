from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    sale_number = serializers.CharField(
        source="sale.sale_number",
        read_only=True,
    )

    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
             "payment_method",
        ]

    def get_customer_name(self, obj):

        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"

        return None