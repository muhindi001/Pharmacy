from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    ACTIONS = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("SALE", "Sale"),
        ("PURCHASE", "Purchase"),
        ("RECEIVED", "Received"),
        ("COMPLETED", "Completed"),
        ("TRANSFER", "Transfer"),
        ("RETURN", "Return"),
        ("ADJUSTMENT", "Adjustment"),
        ("RFID_SCAN", "RFID Scan"),
        ("BARCODE_SCAN", "Barcode Scan"),
        ("EXPORT", "Export"),
        ("OTHER", "Other"),
    )

    action = models.CharField(
        max_length=30,
        choices=ACTIONS,
    )

    module = models.CharField(
        max_length=100,
    )

    object_id = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["module"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.module}"
