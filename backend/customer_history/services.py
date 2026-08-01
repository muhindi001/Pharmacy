from django.db.models import Sum
from django.db.models import Count

from sales.models import Sale


class CustomerHistoryService:

    @staticmethod
    def sales(customer):

        return (
            Sale.objects
            .filter(customer=customer)
            .select_related("customer")
            .prefetch_related(
                "items",
                "items__medicine",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def statistics(customer):

        qs = Sale.objects.filter(customer=customer)

        return {
            "total_sales": qs.count(),

            "total_amount":
                qs.aggregate(
                    Sum("total")
                )["total__sum"] or 0,

            "paid_sales":
                qs.filter(
                    status="Completed"
                ).count(),

            "pending_sales":
                qs.filter(
                    status="Pending"
                ).count(),
        }

    @staticmethod
    def medicine_history(customer):

        return (
            Sale.objects
            .filter(customer=customer)
            .prefetch_related(
                "items",
                "items__medicine",
            )
        )