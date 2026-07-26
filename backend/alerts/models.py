import uuid
from django.db import models


class StockAlert(models.Model):

    ALERT_TYPES = [
        ("Low Stock", "Low Stock"),
        ("Out of Stock", "Out of Stock"),
        ("Expiry", "Expiry"),
        ("Overstock", "Overstock"),
    ]

    STATUS_CHOICES = [
        ("New", "New"),
        ("Read", "Read"),
        ("Resolved", "Resolved"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.CASCADE,
        related_name="stock_alerts",
    )

    batch = models.ForeignKey(
        "batches.Batch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_alerts",
    )

    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
    )

    email_sent = models.BooleanField(
        default=False,
    )

    dashboard_notification = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "stock_alerts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.alert_type} - {self.medicine.medicine_name}"