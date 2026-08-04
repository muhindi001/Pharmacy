import uuid

from rest_framework import serializers

from .models import Payment
from .services import finalize_payment


class PaymentSerializer(serializers.ModelSerializer):

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        status = str(data.get("status") or "").strip().upper()

        if status in {"PAID", "SUCCESS", "SUCCEEDED", "COMPLETED"}:
            normalized_status = "SUCCESS"
        elif status in {"PENDING"}:
            normalized_status = "PENDING"
        elif status in {"FAILED", "FAILURE"}:
            normalized_status = "FAILED"
        else:
            normalized_status = status or "SUCCESS"

        return {
            "transaction_type": "SALE",
            "amount": str(data.get("amount_paid") or data.get("amount") or "0.00"),
            "status": normalized_status,
        }

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

        payment = super().create(validated_data)
        finalize_payment(payment)
        return payment

    def _generate_payment_number(self):
        while True:
            payment_number = f"PAY-{uuid.uuid4().hex[:8].upper()}"
            if not Payment.objects.filter(payment_number=payment_number).exists():
                return payment_number