import uuid

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    sale_number = serializers.CharField(
        source="sale.sale_number",
        read_only=True,
    )

    customer_name = serializers.SerializerMethodField()
    payment_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    status = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_number",
            "sale",
            "sale_number",
            "customer",
            "customer_name",
            "payment_method",
            "amount",
            "amount_paid",
            "balance",
            "currency",
            "transaction_reference",
            "provider",
            "status",
            "payment_date",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["sale_number", "customer_name"]

    def get_customer_name(self, obj):

        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"

        return None

    def validate_payment_number(self, value):
        if value in (None, "", " "):
            return None
        return value

    def validate_status(self, value):
        if value in (None, "", " "):
            return "Pending"

        normalized = str(value).strip()
        status_key = normalized.upper()

        if status_key in {"SUCCESS", "SUCCEEDED", "COMPLETED", "PAID"}:
            return "Paid"
        if status_key == "PENDING":
            return "Pending"
        if status_key == "PARTIAL":
            return "Partial"
        if status_key in {"FAILED", "FAILURE"}:
            return "Failed"
        if status_key in {"REFUNDED", "REFUND"}:
            return "Refunded"
        if status_key in {"CANCELLED", "CANCELED"}:
            return "Cancelled"

        allowed_statuses = {choice[0] for choice in Payment.PAYMENT_STATUS}
        if normalized in allowed_statuses:
            return normalized

        return "Pending"

    def create(self, validated_data):
        payment_number = validated_data.pop("payment_number", None)

        if not payment_number:
            validated_data["payment_number"] = self._generate_payment_number()

        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and getattr(user, "is_authenticated", False):
            validated_data["cashier"] = user
        else:
            raise serializers.ValidationError({"cashier": "Authentication is required to create a payment."})

        return super().create(validated_data)

    def _generate_payment_number(self):
        while True:
            payment_number = f"PAY-{uuid.uuid4().hex[:8].upper()}"
            if not Payment.objects.filter(payment_number=payment_number).exists():
                return payment_number