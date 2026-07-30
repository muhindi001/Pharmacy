from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "created_at",
        "action",
        "module",
        "user",
        "ip_address",
    )

    list_filter = (
        "action",
        "module",
        "created_at",
    )

    search_fields = (
        "description",
        "module",
        "action",
        "user__username",
        "ip_address",
        "object_id",
    )

    readonly_fields = (
        "action",
        "module",
        "object_id",
        "description",
        "user",
        "ip_address",
        "user_agent",
        "metadata",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False