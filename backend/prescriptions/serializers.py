from rest_framework import serializers

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):

    medicine_name = serializers.CharField(
        source="medicine.medicine_name",
        read_only=True,
    )

    class Meta:
        model = PrescriptionItem
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(
        many=True,
        read_only=True,
    )

    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = "__all__"

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"