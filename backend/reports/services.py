from datetime import timedelta
from django.db.models import Avg, Count, Sum, F
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone
from sales.models import Sale, SaleItem
from django.db.models import (
    Sum,
    Count,
    Avg,
    F,
    DecimalField,
    ExpressionWrapper,
    Q,
)
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from inventory.models import Inventory, InventoryTransaction
from django.db.models import (
    Sum,
    Count,
    Avg,
    F,
    Q,
    DecimalField,
    ExpressionWrapper,
)
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from purchases.models import Purchase, PurchaseItem

from customers.models import Customer
from sales.models import Sale

from django.db.models import (
    Sum,
    Count,
    Avg,
    F,
    Q,
)
from suppliers.models import Supplier
from purchases.models import Purchase
from django.db.models import Sum, Count, Avg, F, Q, DecimalField
from sales.models import Sale
from purchases.models import Purchase
from payments.models import Payment


class SalesReportService:

    @staticmethod
    def _filter_queryset(
        queryset,
        start_date=None,
        end_date=None,
        customer=None,
        cashier=None,
        payment_method=None,
        status=None,
    ):

        if start_date:
            queryset = queryset.filter(sale_date__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(sale_date__date__lte=end_date)

        if customer:
            queryset = queryset.filter(customer=customer)

        if cashier:
            queryset = queryset.filter(cashier=cashier)

        if payment_method:
            queryset = queryset.filter(
                payment_method__iexact=payment_method
            )

        if status:
            queryset = queryset.filter(status__iexact=status)

        return queryset

    @staticmethod
    def daily_sales(
        start_date=None,
        end_date=None,
        customer=None,
        cashier=None,
        payment_method=None,
        status=None,
    ):

        queryset = SalesReportService._filter_queryset(
            Sale.objects.all(),
            start_date,
            end_date,
            customer,
            cashier,
            payment_method,
            status,
        )

        return (
            queryset
            .annotate(day=TruncDay("sale_date"))
            .values("day")
            .annotate(
                total_sales=Sum("total_amount"),
                total_profit=Sum("profit"),
                total_orders=Count("id"),
            )
            .order_by("day")
        )

    @staticmethod
    def monthly_sales(
        start_date=None,
        end_date=None,
        customer=None,
        cashier=None,
        payment_method=None,
        status=None,
    ):

        queryset = SalesReportService._filter_queryset(
            Sale.objects.all(),
            start_date,
            end_date,
            customer,
            cashier,
            payment_method,
            status,
        )

        return (
            queryset
            .annotate(month=TruncMonth("sale_date"))
            .values("month")
            .annotate(
                total_sales=Sum("total_amount"),
                total_profit=Sum("profit"),
                total_orders=Count("id"),
            )
            .order_by("month")
        )

    @staticmethod
    def yearly_sales(
        start_date=None,
        end_date=None,
        customer=None,
        cashier=None,
        payment_method=None,
        status=None,
    ):

        queryset = SalesReportService._filter_queryset(
            Sale.objects.all(),
            start_date,
            end_date,
            customer,
            cashier,
            payment_method,
            status,
        )

        return (
            queryset
            .annotate(year=TruncYear("sale_date"))
            .values("year")
            .annotate(
                total_sales=Sum("total_amount"),
                total_profit=Sum("profit"),
                total_orders=Count("id"),
            )
            .order_by("year")
        )

    @staticmethod
    def sales_summary(
        start_date=None,
        end_date=None,
        customer=None,
        cashier=None,
        payment_method=None,
        status=None,
    ):

        queryset = SalesReportService._filter_queryset(
            Sale.objects.all(),
            start_date,
            end_date,
            customer,
            cashier,
            payment_method,
            status,
        )

        return queryset.aggregate(
            total_sales=Sum("total_amount"),
            total_profit=Sum("profit"),
            total_orders=Count("id"),
            average_sale=Avg("total_amount"),
        )

    @staticmethod
    def sales_by_product(
        start_date=None,
        end_date=None,
    ):

        queryset = SaleItem.objects.select_related(
            "medicine",
            "sale",
        )

        if start_date:
            queryset = queryset.filter(
                sale__sale_date__date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                sale__sale_date__date__lte=end_date
            )

        return (
            queryset
            .values(
                "medicine__id",
                "medicine__medicine_name",
                "medicine__generic_name",
            )
            .annotate(
                quantity_sold=Sum("quantity"),
                total_sales=Sum("total"),
                total_profit=Sum("profit"),
            )
            .order_by("-quantity_sold")
        )

    @staticmethod
    def sales_by_category(
        start_date=None,
        end_date=None,
    ):

        queryset = SaleItem.objects.select_related(
            "medicine__category",
            "sale",
        )

        if start_date:
            queryset = queryset.filter(
                sale__sale_date__date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                sale__sale_date__date__lte=end_date
            )

        return (
            queryset
            .values(
                "medicine__category__id",
                "medicine__category__name",
            )
            .annotate(
                quantity=Sum("quantity"),
                total_sales=Sum("total"),
            )
            .order_by("-total_sales")
        )

    @staticmethod
    def top_selling_medicines(
        limit=10,
        start_date=None,
        end_date=None,
    ):

        queryset = SaleItem.objects.select_related(
            "medicine",
            "sale",
        )

        if start_date:
            queryset = queryset.filter(
                sale__sale_date__date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                sale__sale_date__date__lte=end_date
            )

        return (
            queryset
            .values(
                "medicine__id",
                "medicine__medicine_name",
                "medicine__generic_name",
            )
            .annotate(
                quantity=Sum("quantity"),
                revenue=Sum("total"),
                profit=Sum("profit"),
            )
            .order_by("-quantity")[:limit]
        )

# inventory_report

class InventoryReportService:

    @staticmethod
    def current_stock(search=None, category=None):

        queryset = Inventory.objects.select_related(
            "medicine",
            "medicine__category",
            "batch",
        )

        if search:
            queryset = queryset.filter(
                Q(medicine__medicine_name__icontains=search)
                | Q(medicine__generic_name__icontains=search)
                | Q(medicine__barcode__icontains=search)
                | Q(medicine__sku__icontains=search)
            )

        if category:
            queryset = queryset.filter(
                medicine__category_id=category
            )

        return queryset.order_by(
            "medicine__medicine_name"
        )
    @staticmethod
    def inventory_valuation():

        return Inventory.objects.aggregate(

            total_quantity=Sum("quantity"),

            buying_value=Sum(

                ExpressionWrapper(

                    F("quantity")
                    * F("medicine__buying_price"),

                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )

            ),

            selling_value=Sum(

                ExpressionWrapper(

                    F("quantity")
                    * F("medicine__selling_price"),

                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )

            ),

        )
        
    @staticmethod
    def low_stock():

        return Inventory.objects.filter(

            quantity__lte=F("minimum_level")

        ).select_related(

            "medicine",
            "batch",
        )
    @staticmethod
    def out_of_stock():

        return Inventory.objects.filter(

            quantity=0

        ).select_related(

            "medicine",
            "batch",
        )
    @staticmethod
    def expiring_medicines(days=30):

        today = timezone.now().date()

        expiry = today + timedelta(days=days)

        return Inventory.objects.filter(

            batch__expiry_date__range=[today, expiry]

        ).select_related(

            "medicine",
            "batch",
        )
    @staticmethod
    def expired_medicines():

        today = timezone.now().date()

        return Inventory.objects.filter(

            batch__expiry_date__lt=today

        ).select_related(

            "medicine",
            "batch",
        )
    @staticmethod
    def stock_movement(

        start_date=None,
        end_date=None,

    ):

        queryset = InventoryTransaction.objects.select_related(

            "inventory",
            "inventory__medicine",

        )

        if start_date:

            queryset = queryset.filter(

                created_at__date__gte=start_date

            )

        if end_date:

            queryset = queryset.filter(

                created_at__date__lte=end_date

            )

        return (

            queryset

            .annotate(

                day=TruncDay("created_at")

            )

            .values(

                "day",
                "transaction_type",

            )

            .annotate(

                quantity=Sum("quantity"),

                total_transactions=Count("id"),

            )

            .order_by("day")

        )
    @staticmethod
    def inventory_summary():

        today = timezone.now().date()

        next_month = today + timedelta(days=30)

        return {

            "total_items": Inventory.objects.count(),

            "total_quantity": Inventory.objects.aggregate(

                total=Sum("quantity")

            )["total"] or 0,

            "low_stock": Inventory.objects.filter(

                quantity__lte=F("minimum_level")

            ).count(),

            "out_of_stock": Inventory.objects.filter(

                quantity=0

            ).count(),

            "expiring": Inventory.objects.filter(

                batch__expiry_date__range=[today, next_month]

            ).count(),

            "expired": Inventory.objects.filter(

                batch__expiry_date__lt=today

            ).count(),

        }
# purchase_report
class PurchaseReportService:

    @staticmethod
    def _filter_queryset(
        queryset,
        start_date=None,
        end_date=None,
        supplier=None,
        status=None,
        payment_status=None,
    ):

        if start_date:
            queryset = queryset.filter(
                purchase_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                purchase_date__lte=end_date
            )

        if supplier:
            queryset = queryset.filter(
                supplier_id=supplier
            )

        if status:
            queryset = queryset.filter(
                status__iexact=status
            )

        if payment_status:
            queryset = queryset.filter(
                payment_status__iexact=payment_status
            )

        return queryset
    @staticmethod
    def purchase_summary(
        start_date=None,
        end_date=None,
        supplier=None,
        status=None,
        payment_status=None,
    ):

        queryset = PurchaseReportService._filter_queryset(
            Purchase.objects.all(),
            start_date,
            end_date,
            supplier,
            status,
            payment_status,
        )

        return queryset.aggregate(

            total_purchase=Sum("total"),

            total_orders=Count("id"),

            average_purchase=Avg("total"),

            total_paid=Sum("paid_amount"),

            total_due=Sum("balance"),

        )
    @staticmethod
    def daily_purchases(
        start_date=None,
        end_date=None,
    ):

        queryset = PurchaseReportService._filter_queryset(
            Purchase.objects.all(),
            start_date,
            end_date,
        )

        return (
            queryset
            .annotate(day=TruncDay("purchase_date"))
            .values("day")
            .annotate(

                total_purchase=Sum("total"),

                total_orders=Count("id"),

            )
            .order_by("day")
        )
    @staticmethod
    def monthly_purchases(
        start_date=None,
        end_date=None,
    ):

        queryset = PurchaseReportService._filter_queryset(
            Purchase.objects.all(),
            start_date,
            end_date,
        )

        return (
            queryset
            .annotate(month=TruncMonth("purchase_date"))
            .values("month")
            .annotate(

                total_purchase=Sum("total"),

                total_orders=Count("id"),

            )
            .order_by("month")
        )
    @staticmethod
    def yearly_purchases(
        start_date=None,
        end_date=None,
    ):

        queryset = PurchaseReportService._filter_queryset(
            Purchase.objects.all(),
            start_date,
            end_date,
        )

        return (
            queryset
            .annotate(year=TruncYear("purchase_date"))
            .values("year")
            .annotate(

                total_purchase=Sum("total"),

                total_orders=Count("id"),

            )
            .order_by("year")
        )
    @staticmethod
    def purchases_by_supplier(
        start_date=None,
        end_date=None,
    ):

        queryset = PurchaseItem.objects.select_related(
            "purchase",
            "purchase__supplier",
        )

        if start_date:
            queryset = queryset.filter(
                purchase__purchase_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                purchase__purchase_date__lte=end_date
            )

        return (
            queryset
            .values(
                "purchase__supplier__id",
                "purchase__supplier__supplier_name",
            )
            .annotate(

                total_purchase=Sum("total"),

                quantity=Sum("quantity"),

                orders=Count("purchase", distinct=True),

            )
            .order_by("-total_purchase")
        )
    @staticmethod
    def purchase_cost_analysis(
        start_date=None,
        end_date=None,
    ):

        queryset = PurchaseItem.objects.select_related(
            "medicine",
            "purchase",
        )

        if start_date:
            queryset = queryset.filter(
                purchase__purchase_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                purchase__purchase_date__lte=end_date
            )

        return (
            queryset
            .values(
                "medicine__medicine_name",
                "medicine__generic_name",
            )
            .annotate(

                total_quantity=Sum("quantity"),

                total_cost=Sum("total"),

                average_price=Avg("unit_price"),

            )
            .order_by("-total_cost")
        )
    @staticmethod
    def top_purchased_medicines(
        limit=10,
    ):

        return (
            PurchaseItem.objects
            .values(
                "medicine__medicine_name",
                "medicine__generic_name",
            )
            .annotate(

                quantity=Sum("quantity"),

                total_cost=Sum("total"),

            )
            .order_by("-quantity")[:limit]
        )
    @staticmethod
    def outstanding_purchases():

        return Purchase.objects.filter(

            balance__gt=0

        ).select_related(

            "supplier"

        )
    @staticmethod
    def search(query):

        return Purchase.objects.filter(

            Q(purchase_number__icontains=query)
            | Q(invoice_number__icontains=query)
            | Q(supplier__supplier_name__icontains=query)

        )

class CustomerReportService:

    @staticmethod
    def purchase_history(
        customer=None,
        start_date=None,
        end_date=None,
    ):

        queryset = Sale.objects.select_related(
            "customer"
        )

        if customer:
            queryset = queryset.filter(customer_id=customer)

        if start_date:
            queryset = queryset.filter(
                sale_date__date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                sale_date__date__lte=end_date
            )

        return queryset.order_by("-sale_date")

    @staticmethod
    def customer_summary():

        return Customer.objects.annotate(

            total_orders=Count("sale"),

            total_spent=Sum("sale__total_amount"),

            average_order=Avg("sale__total_amount"),

        ).order_by("-total_spent")

    @staticmethod
    def top_customers(limit=10):

        return Customer.objects.annotate(

            total_spent=Sum("sale__total_amount"),

            total_orders=Count("sale"),

        ).order_by("-total_spent")[:limit]

    @staticmethod
    def outstanding_credit():

        return Customer.objects.filter(

            balance__gt=0

        ).order_by("-balance")

    @staticmethod
    def search(query):

        return Customer.objects.filter(

            Q(first_name__icontains=query)

            | Q(last_name__icontains=query)

            | Q(phone_number__icontains=query)

            | Q(email__icontains=query)

        )

class SupplierReportService:

    @staticmethod
    def supplier_summary():

        return Supplier.objects.annotate(

            total_orders=Count("purchase"),

            total_purchase=Sum("purchase__total"),

            average_purchase=Avg("purchase__total"),

        ).order_by("-total_purchase")

    @staticmethod
    def supplier_purchase_history(

        supplier=None,

        start_date=None,

        end_date=None,

    ):

        queryset = Purchase.objects.select_related(
            "supplier"
        )

        if supplier:
            queryset = queryset.filter(
                supplier_id=supplier
            )

        if start_date:
            queryset = queryset.filter(
                purchase_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                purchase_date__lte=end_date
            )

        return queryset.order_by("-purchase_date")

    @staticmethod
    def top_suppliers(limit=10):

        return Supplier.objects.annotate(

            total_purchase=Sum("purchase__total"),

            total_orders=Count("purchase"),

        ).order_by("-total_purchase")[:limit]

    @staticmethod
    def outstanding_suppliers():

        return Purchase.objects.filter(

            balance__gt=0

        ).select_related("supplier")

    @staticmethod
    def search(query):

        return Supplier.objects.filter(

            Q(supplier_name__icontains=query)

            | Q(company_name__icontains=query)

            | Q(phone_number__icontains=query)

            | Q(email__icontains=query)

        )
class FinancialReportService:

    @staticmethod
    def _sales_queryset(start_date=None, end_date=None):

        queryset = Sale.objects.all()

        if start_date:
            queryset = queryset.filter(
                sale_date__date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                sale_date__date__lte=end_date
            )

        return queryset

    @staticmethod
    def _purchase_queryset(start_date=None, end_date=None):

        queryset = Purchase.objects.all()

        if start_date:
            queryset = queryset.filter(
                purchase_date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                purchase_date__lte=end_date
            )

        return queryset
    @staticmethod
    def revenue(
        start_date=None,
        end_date=None,
    ):

        queryset = FinancialReportService._sales_queryset(
            start_date,
            end_date,
        )

        return queryset.aggregate(

            total_sales=Sum("total_amount"),

            total_profit=Sum("profit"),

            total_orders=Count("id"),

            average_sale=Avg("total_amount"),

        )
    @staticmethod
    def profit_loss(
        start_date=None,
        end_date=None,
    ):

        sales = FinancialReportService._sales_queryset(
            start_date,
            end_date,
        )

        purchases = FinancialReportService._purchase_queryset(
            start_date,
            end_date,
        )

        revenue = sales.aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        purchase_cost = purchases.aggregate(
            total=Sum("total")
        )["total"] or 0

        gross_profit = revenue - purchase_cost

        return {

            "revenue": revenue,

            "purchase_cost": purchase_cost,

            "gross_profit": gross_profit,

        }
    @staticmethod
    def cash_flow(
        start_date=None,
        end_date=None,
    ):

        sales = FinancialReportService._sales_queryset(
            start_date,
            end_date,
        )

        purchases = FinancialReportService._purchase_queryset(
            start_date,
            end_date,
        )

        cash_in = sales.aggregate(
            total=Sum("paid_amount")
        )["total"] or 0

        cash_out = purchases.aggregate(
            total=Sum("paid_amount")
        )["total"] or 0

        return {

            "cash_in": cash_in,

            "cash_out": cash_out,

            "net_cash_flow": cash_in - cash_out,

        }
    @staticmethod
    def payment_methods(
        start_date=None,
        end_date=None,
    ):

        queryset = FinancialReportService._sales_queryset(
            start_date,
            end_date,
        )

        return (

            queryset

            .values("payment_method")

            .annotate(

                total_sales=Sum("total_amount"),

                transactions=Count("id"),

            )

            .order_by("-total_sales")

        )
    @staticmethod
    def tax_summary(
        start_date=None,
        end_date=None,
    ):

        queryset = FinancialReportService._sales_queryset(
            start_date,
            end_date,
        )

        return queryset.aggregate(

            taxable_sales=Sum("subtotal"),

            total_tax=Sum("tax_amount"),

            total_discount=Sum("discount"),

        )
    @staticmethod
    def receivables():

        return Sale.objects.filter(

            balance__gt=0

        ).values(

            "invoice_number",

            "customer__first_name",

            "balance",

            "sale_date",

        )
    @staticmethod
    def payables():

        return Purchase.objects.filter(

            balance__gt=0

        ).values(

            "purchase_number",

            "supplier__supplier_name",

            "balance",

            "purchase_date",

        )
    @staticmethod
    def dashboard():

        revenue = Sale.objects.aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        purchases = Purchase.objects.aggregate(
            total=Sum("total")
        )["total"] or 0

        profit = Sale.objects.aggregate(
            total=Sum("profit")
        )["total"] or 0

        customers = Sale.objects.values(
            "customer"
        ).distinct().count()

        return {

            "revenue": revenue,

            "purchase_cost": purchases,

            "profit": profit,

            "customers": customers,

            "sales": Sale.objects.count(),

            "purchases": Purchase.objects.count(),

        }