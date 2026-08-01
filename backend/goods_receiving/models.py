from django.db import models
from django.conf import settings
from django.utils import timezone

from purchases.models import Purchase
from medicines.models import Medicine
from batches.models import Batch
from inventory.models import Inventory
from suppliers.models import Supplier
from warehouses.models import Warehouse


class GoodsReceipt(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("RECEIVED", "Received"),
        ("CANCELLED", "Cancelled"),
    )

    grn_number = models.CharField(
        max_length=30,
        unique=True
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.PROTECT,
        related_name="goods_receipts",
        null=True,
        blank=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="goods_receipts"
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="goods_receipts"
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True
    )

    delivery_note = models.CharField(
        max_length=100,
        blank=True
    )

    received_date = models.DateTimeField(
        default=timezone.now
    )

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="received_goods"
    )

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-received_date"]

    def __str__(self):
        return self.grn_number


class GoodsReceiptItem(models.Model):

    receipt = models.ForeignKey(
        GoodsReceipt,
        on_delete=models.CASCADE,
        related_name="items"
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )

    batch_number = models.CharField(max_length=100)

    manufacturing_date = models.DateField()

    expiry_date = models.DateField()

    ordered_quantity = models.PositiveIntegerField(default=0)

    received_quantity = models.PositiveIntegerField()

    accepted_quantity = models.PositiveIntegerField()

    rejected_quantity = models.PositiveIntegerField(default=0)

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    shelf_location = models.CharField(
        max_length=100,
        blank=True
    )

    inventory_updated = models.BooleanField(default=False)

    class Meta:
        ordering = ["medicine__medicine_name"]

    def __str__(self):
        return f"{self.medicine} - {self.batch_number}"