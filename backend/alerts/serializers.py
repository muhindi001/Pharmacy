from rest_framework import serializers
from .models import StockAlert


class StockAlertSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    class Meta:
        model = StockAlert
        fields = "__all__"