from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "email",
        "username",
        "role",
        "status",
        "is_verified",
        "is_staff",
    )

    list_filter = (
        "role",
        "status",
        "is_verified",
        "is_staff",
    )

    search_fields = (
        "email",
        "username",
        "phone_number",
    )

    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone_number",
                    "profile_image",
                    "role",
                    "status",
                    "is_verified",
                    "two_factor_enabled",
                    "last_login_ip",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login_ip",
    )