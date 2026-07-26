from rest_framework import serializers

from .models import Invoice, Receipt


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):

    receipts = ReceiptSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Invoice
        fields = "__all__"