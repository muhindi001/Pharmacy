import uuid

from django.db import models


class SalesReturn(models.Model):

    RETURN_TYPES = [
        ("Full", "Full"),
        ("Partial", "Partial"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    return_number = models.CharField(
        max_length=30,
        unique=True,
    )

    sale = models.ForeignKey(
        "sales.Sale",
        on_delete=models.PROTECT,
        related_name="returns",
    )

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_returns",
    )

    return_type = models.CharField(
        max_length=20,
        choices=RETURN_TYPES,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_returns",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    return_date = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "sales_returns"
        ordering = ["-return_date"]

    def __str__(self):
        return self.return_number


class SalesReturnItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sales_return = models.ForeignKey(
        SalesReturn,
        on_delete=models.CASCADE,
        related_name="items",
    )

    sale_item = models.ForeignKey(
        "sales.SaleItem",
        on_delete=models.PROTECT,
        related_name="returned_items",
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
    )

    batch = models.ForeignKey(
        "batches.Batch",
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "sales_return_items"

    def __str__(self):
        return self.medicine.medicine_name