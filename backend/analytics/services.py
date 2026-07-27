from datetime import timedelta

from django.db.models import (
    Sum,
    Count,
    Avg,
    F,
    DecimalField,
    ExpressionWrapper,
)
from django.db.models.functions import TruncDate
from django.utils import timezone

from sales.models import Sale, SaleItem
from purchases.models import Purchase
from inventory.models import Inventory
from medicines.models import Medicine
from customers.models import Customer
from suppliers.models import Supplier
from payments.models import Payment


class DashboardAnalyticsService:

    @staticmethod
    def dashboard():

        today = timezone.now().date()

        today_sales = Sale.objects.filter(
            sale_date__date=today
        )

        today_revenue = (
            today_sales.aggregate(
                total=Sum("grand_total")
            )["total"] or 0
        )

        today_profit = (
            today_sales.aggregate(
                total=Sum("profit")
            )["total"] or 0
        )

        inventory_value = (
            Inventory.objects.aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("quantity") * F("medicine__buying_price"),
                        output_field=DecimalField(
                            max_digits=18,
                            decimal_places=2,
                        ),
                    )
                )
            )["total"] or 0
        )

        return {

            "today_sales": today_sales.count(),

            "today_revenue": today_revenue,

            "today_profit": today_profit,

            "customers": Customer.objects.count(),

            "suppliers": Supplier.objects.count(),

            "medicines": Medicine.objects.count(),

            "inventory_value": inventory_value,

            "low_stock": Inventory.objects.filter(
                quantity__lte=F("minimum_level")
            ).count(),

            "out_of_stock": Inventory.objects.filter(
                quantity=0
            ).count(),

        }


class SalesAnalyticsService:

    @staticmethod
    def daily_sales(days=30):

        start = timezone.now().date() - timedelta(days=days)

        return (

            Sale.objects

            .filter(
                sale_date__date__gte=start
            )

            .annotate(
                day=TruncDate("sale_date")
            )

            .values("day")

            .annotate(

                revenue=Sum("grand_total"),

                profit=Sum("profit"),

                transactions=Count("id"),

            )

            .order_by("day")

        )

    @staticmethod
    def top_selling(limit=10):

        return (

            SaleItem.objects

            .values(

                "medicine__medicine_name",

                "medicine__generic_name",

            )

            .annotate(

                quantity=Sum("quantity"),

                revenue=Sum("total"),

            )

            .order_by("-quantity")[:limit]

        )

    @staticmethod
    def average_sale():

        return Sale.objects.aggregate(

            average=Avg("grand_total")

        )


class InventoryAnalyticsService:

    @staticmethod
    def stock_summary():

        return {

            "total_items": Inventory.objects.count(),

            "total_quantity":

                Inventory.objects.aggregate(

                    total=Sum("quantity")

                )["total"] or 0,

            "low_stock":

                Inventory.objects.filter(

                    quantity__lte=F("minimum_level")

                ).count(),

            "out_of_stock":

                Inventory.objects.filter(

                    quantity=0

                ).count(),

        }

    @staticmethod
    def inventory_value():

        return Inventory.objects.aggregate(

            total=Sum(

                ExpressionWrapper(

                    F("quantity") *

                    F("medicine__buying_price"),

                    output_field=DecimalField(

                        max_digits=18,

                        decimal_places=2,

                    ),

                )

            )

        )


class FinancialAnalyticsService:

    @staticmethod
    def overview():

        revenue = (

            Sale.objects.aggregate(

                total=Sum("grand_total")

            )["total"] or 0

        )

        profit = (

            Sale.objects.aggregate(

                total=Sum("profit")

            )["total"] or 0

        )

        purchases = (

            Purchase.objects.aggregate(

                total=Sum("grand_total")

            )["total"] or 0

        )

        payments = (

            Payment.objects.aggregate(

                total=Sum("amount")

            )["total"] or 0

        )

        return {

            "revenue": revenue,

            "profit": profit,

            "purchase_cost": purchases,

            "payments_received": payments,

        }


class CustomerAnalyticsService:

    @staticmethod
    def overview():

        return {

            "total_customers":

                Customer.objects.count(),

            "active_customers":

                Customer.objects.filter(

                    is_active=True

                ).count(),

        }


class SupplierAnalyticsService:

    @staticmethod
    def overview():

        return {

            "total_suppliers":

                Supplier.objects.count(),

            "active_suppliers":

                Supplier.objects.filter(

                    status=True

                ).count(),

        }


class BusinessIntelligenceService:

    @staticmethod
    def fast_moving(limit=10):

        return (

            SaleItem.objects

            .values(

                "medicine__medicine_name"

            )

            .annotate(

                quantity=Sum("quantity")

            )

            .order_by("-quantity")[:limit]

        )

    @staticmethod
    def slow_moving(limit=10):

        return (

            SaleItem.objects

            .values(

                "medicine__medicine_name"

            )

            .annotate(

                quantity=Sum("quantity")

            )

            .order_by("quantity")[:limit]

        )

    @staticmethod
    def dead_stock():

        return Inventory.objects.filter(

            quantity__gt=0,

            medicine__saleitem__isnull=True,

        ).distinct()


class ForecastService:

    @staticmethod
    def sales_forecast(days=30):

        average = (

            Sale.objects.aggregate(

                avg=Avg("grand_total")

            )["avg"] or 0

        )

        return {

            "forecast_days": days,

            "estimated_revenue": average * days,

            "average_daily_sales": average,

        }