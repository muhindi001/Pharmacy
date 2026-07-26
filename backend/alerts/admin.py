from django.contrib import admin
from .models import StockAlert


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):

    list_display = (
        "medicine",
        "alert_type",
        "status",
        "email_sent",
        "created_at",
    )

    search_fields = (
        "medicine__medicine_name",
        "message",
    )

    list_filter = (
        "alert_type",
        "status",
        "email_sent",
    )