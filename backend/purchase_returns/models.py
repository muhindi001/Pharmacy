import uuid
from django.db import models


class PurchaseReturn(models.Model):

    RETURN_TYPES = [
        ("Full", "Full"),
        ("Partial", "Partial"),
    ]

    STATUS = [
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

    purchase = models.ForeignKey(
        "purchases.Purchase",
        on_delete=models.PROTECT,
        related_name="purchase_returns",
    )

    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="purchase_returns",
    )

    return_type = models.CharField(
        max_length=20,
        choices=RETURN_TYPES,
    )

    reason = models.TextField()

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending",
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_purchase_returns",
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
        db_table = "purchase_returns"
        ordering = ["-return_date"]

    def __str__(self):
        return self.return_number


class PurchaseReturnItem(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    purchase_return = models.ForeignKey(
        PurchaseReturn,
        on_delete=models.CASCADE,
        related_name="items",
    )

    purchase_item = models.ForeignKey(
        "purchases.PurchaseItem",
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

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "purchase_return_items"

    def __str__(self):
        return self.medicine.medicine_name