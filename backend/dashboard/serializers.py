from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    today_sales = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    monthly_sales = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_profit = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_purchases = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    inventory_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_customers = serializers.IntegerField()

    total_suppliers = serializers.IntegerField()

    total_medicines = serializers.IntegerField()

    low_stock = serializers.IntegerField()

    expiring_soon = serializers.IntegerField()

    out_of_stock = serializers.IntegerField()