from rest_framework import serializers
from .models import StockAlert


class StockAlertSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(source="medicine.medicine_name", read_only=True)
    medicine_generic_name = serializers.CharField(
        source="medicine.generic_name",
        read_only=True,
        allow_null=True,
    )
    batch_number = serializers.CharField(source="batch.batch_number", read_only=True, allow_null=True)

    class Meta:
        model = StockAlert
        fields = [
            "id",
            "medicine_name",
            "medicine_generic_name",
            "batch",
            "batch_number",
            "alert_type",
            "message",
            "status",
            "email_sent",
            "dashboard_notification",
            "created_at",
            "updated_at",
        ]