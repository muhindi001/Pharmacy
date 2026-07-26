from rest_framework import serializers


class ReportFilterSerializer(serializers.Serializer):

    start_date = serializers.DateField(required=False)

    end_date = serializers.DateField(required=False)

    supplier = serializers.UUIDField(required=False)

    customer = serializers.UUIDField(required=False)

    category = serializers.UUIDField(required=False)

    medicine = serializers.UUIDField(required=False)

    cashier = serializers.UUIDField(required=False)

    payment_method = serializers.CharField(required=False)

    status = serializers.CharField(required=False)