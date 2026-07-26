from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "payment_number",
        "sale",
        "payment_method",
        "amount",
        "status",
        "payment_date",
    )

    search_fields = (
        "payment_number",
        "transaction_reference",
    )

    list_filter = (
        "payment_method",
        "status",
    )