from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "customer_code",
        "first_name",
        "last_name",
        "phone_number",
        "loyalty_points",
        "loyalty_tier",
        "status",
    )

    search_fields = (
        "customer_code",
        "first_name",
        "last_name",
        "phone_number",
        "email",
    )

    list_filter = (
        "status",
        "loyalty_tier",
    )

    ordering = (
        "first_name",
    )