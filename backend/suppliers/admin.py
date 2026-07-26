from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "supplier_name",
        "company_name",
        "contact_person",
        "phone_number",
        "payment_terms",
        "is_active",
    )

    search_fields = (
        "supplier_name",
        "company_name",
        "contact_person",
        "phone_number",
        "email",
    )

    list_filter = (
        "payment_terms",
        "is_active",
    )

    ordering = (
        "supplier_name",
    )