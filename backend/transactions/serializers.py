from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.customer_name",
        read_only=True,
    )

    cashier_name = serializers.CharField(
        source="cashier.username",
        read_only=True,
    )

    class Meta:
        model = Transaction

        fields = (
            "id",
            "transaction_number",
            "sale",
            "payment",
            "customer",
            "customer_name",
            "cashier",
            "cashier_name",
            "transaction_type",
            "payment_method",
            "amount",
            "reference_number",
            "description",
            "status",
            "transaction_date",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "transaction_number",
            "created_at",
            "updated_at",
        )