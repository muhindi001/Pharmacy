from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_number",
        "transaction_type",
        "customer",
        "amount",
        "payment_method",
        "status",
        "transaction_date",
    )

    list_filter = (
        "transaction_type",
        "payment_method",
        "status",
        "transaction_date",
    )

    search_fields = (
        "transaction_number",
        "reference_number",
        "customer__customer_name",
    )

    readonly_fields = (
        "transaction_number",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-transaction_date",
    )

    date_hierarchy = "transaction_date"

    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    "transaction_number",
                    "transaction_type",
                    "status",
                    "transaction_date",
                )
            },
        ),
        (
            "Relationships",
            {
                "fields": (
                    "sale",
                    "payment",
                    "customer",
                    "cashier",
                )
            },
        ),
        (
            "Financial Information",
            {
                "fields": (
                    "amount",
                    "payment_method",
                    "reference_number",
                    "description",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )