from rest_framework import serializers

from .models import Invoice, Receipt


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):

    customer_name = serializers.SerializerMethodField()
    receipts = ReceiptSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "sale",
            "customer",
            "customer_name",
            "payment",
            "invoice_date",
            "due_date",
            "subtotal",
            "discount",
            "tax",
            "total",
            "status",
            "qr_code",
            "pdf",
            "notes",
            "created_at",
            "updated_at",
            "receipts",
        ]

    def get_customer_name(self, obj):
        customer = getattr(obj, "customer", None)
        if customer is None:
            return None
        if getattr(customer, "first_name", None) or getattr(customer, "last_name", None):
            return f"{customer.first_name or ''} {customer.last_name or ''}".strip()
        return str(customer)
