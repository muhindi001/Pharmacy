from rest_framework import serializers


class DashboardAnalyticsSerializer(serializers.Serializer):
    today_sales = serializers.IntegerField()
    today_revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    today_profit = serializers.DecimalField(max_digits=18, decimal_places=2)
    customers = serializers.IntegerField()
    suppliers = serializers.IntegerField()
    medicines = serializers.IntegerField()
    inventory_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    low_stock = serializers.IntegerField()
    out_of_stock = serializers.IntegerField()


class DailySalesSerializer(serializers.Serializer):
    day = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    profit = serializers.DecimalField(max_digits=18, decimal_places=2)
    transactions = serializers.IntegerField()


class TopSellingSerializer(serializers.Serializer):
    medicine__medicine_name = serializers.CharField()
    medicine__generic_name = serializers.CharField()
    quantity = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=18, decimal_places=2)


class AverageSaleSerializer(serializers.Serializer):
    average = serializers.DecimalField(max_digits=18, decimal_places=2)


class InventorySummarySerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    low_stock = serializers.IntegerField()
    out_of_stock = serializers.IntegerField()


class InventoryValueSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=18, decimal_places=2)


class FinancialOverviewSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    profit = serializers.DecimalField(max_digits=18, decimal_places=2)
    purchase_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    payments_received = serializers.DecimalField(max_digits=18, decimal_places=2)


class CustomerOverviewSerializer(serializers.Serializer):
    total_customers = serializers.IntegerField()
    active_customers = serializers.IntegerField()


class SupplierOverviewSerializer(serializers.Serializer):
    total_suppliers = serializers.IntegerField()
    active_suppliers = serializers.IntegerField()


class FastMovingSerializer(serializers.Serializer):
    medicine__medicine_name = serializers.CharField()
    quantity = serializers.IntegerField()


class SlowMovingSerializer(serializers.Serializer):
    medicine__medicine_name = serializers.CharField()
    quantity = serializers.IntegerField()


class DeadStockSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    medicine = serializers.CharField(source="medicine.medicine_name")
    quantity = serializers.IntegerField()


class ForecastSerializer(serializers.Serializer):
    forecast_days = serializers.IntegerField()
    estimated_revenue = serializers.DecimalField(max_digits=18, decimal_places=2)
    average_daily_sales = serializers.DecimalField(max_digits=18, decimal_places=2)