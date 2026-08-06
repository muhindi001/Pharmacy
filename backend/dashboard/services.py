from datetime import date, timedelta

from django.db.models import Count, F, Sum

from customers.models import Customer
from inventory.models import Inventory
from medicines.models import Medicine
from purchases.models import Purchase
from sales.models import Sale, SaleItem
from suppliers.models import Supplier


class DashboardService:

    @staticmethod
    def get_dashboard():

        today = date.today()

        today_sales = (
            Sale.objects.filter(
                created_at__date=today,
            ).aggregate(
                total=Sum("total"),
            )["total"] or 0
        )

        monthly_sales = (
            Sale.objects.filter(
                created_at__year=today.year,
                created_at__month=today.month,
            ).aggregate(
                total=Sum("total"),
            )["total"] or 0
        )

        purchases = (
            Purchase.objects.aggregate(
                total=Sum("total"),
            )["total"] or 0
        )

        inventory_value = (
            Inventory.objects.aggregate(
                total=Sum(
                    F("quantity") * F("medicine__buying_price")
                )
            )["total"] or 0
        )

        total_profit = (
            SaleItem.objects.aggregate(
                total=Sum("profit"),
            )["total"] or 0
        )

        return {

            "today_sales": today_sales,

            "monthly_sales": monthly_sales,

            "total_revenue": monthly_sales,

            "total_profit": total_profit,

            "total_purchases": purchases,

            "inventory_value": inventory_value,

            "total_customers": Customer.objects.count(),

            "total_suppliers": Supplier.objects.count(),

            "total_medicines": Medicine.objects.count(),

            "low_stock": Inventory.objects.filter(
                quantity__lte=F("minimum_level")
            ).count(),

            "expiring_soon": Inventory.objects.filter(
                batch__expiry_date__lte=(today + timedelta(days=30))
            ).count(),

            "out_of_stock": Inventory.objects.filter(
                quantity=0
            ).count(),
        }