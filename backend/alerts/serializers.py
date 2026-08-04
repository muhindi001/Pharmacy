from rest_framework import serializers
from .models import StockAlert


class StockAlertSerializer(serializers.ModelSerializer):

    medicine = serializers.SerializerMethodField(read_only=True)

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    batch_number = serializers.CharField(
        source="batch.batch_number",
        read_only=True,
    )

    def get_medicine(self, obj):
        return obj.medicine.medicine_name if obj.medicine else None

    class Meta:
        model = StockAlert
        fields = "__all__"