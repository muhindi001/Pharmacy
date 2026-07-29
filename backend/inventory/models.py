import uuid
from django.db import models
from warehouses.models import Warehouse

class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = [
        ("Stock In", "Stock In"),
        ("Stock Out", "Stock Out"),
        ("Adjustment", "Adjustment"),
        ("Transfer", "Transfer"),
        ("Customer Return", "Customer Return"),
        ("Supplier Return", "Supplier Return"),
        ("Damage", "Damage"),
        ("Expired", "Expired"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    batch = models.ForeignKey(
        "batches.Batch",
        on_delete=models.PROTECT,
        related_name="inventory_transactions",
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="inventory_transactions",
    )
    rfid_tag = models.ForeignKey(
        "rfid.RFIDTag",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    scanned_by_reader = models.ForeignKey(
        "rfid.RFIDReader",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPES,
    )

    quantity = models.PositiveIntegerField()

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="inventory_transactions",
    )

    transaction_date = models.DateTimeField(
        auto_now_add=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "inventory_transactions"
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.transaction_type} - {self.medicine.medicine_name}"
    
# Inventory
class Inventory(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    current_location = models.CharField(
        max_length=150,
        blank=True
    )

    last_rfid_scan = models.DateTimeField(
        null=True,
        blank=True
    )

    batch = models.OneToOneField(
        "batches.Batch",
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    warehouse = models.ForeignKey(
        "warehouses.Warehouse",
    on_delete=models.PROTECT,
    related_name="inventory",
)

    quantity = models.PositiveIntegerField(
        default=0,
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0,
    )

    available_quantity = models.PositiveIntegerField(
        default=0,
    )

    reorder_level = models.PositiveIntegerField(
        default=10,
    )

    maximum_level = models.PositiveIntegerField(
        default=1000,
    )

    minimum_level = models.PositiveIntegerField(
        default=10,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    last_stock_in = models.DateTimeField(
        blank=True,
        null=True,
    )

    last_stock_out = models.DateTimeField(
        blank=True,
        null=True,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "inventory"
        ordering = [
            "medicine__medicine_name",
        ]

    def __str__(self):
        return (
            f"{self.medicine.medicine_name} - "
            f"{self.quantity}"
        )

    def save(self, *args, **kwargs):
        self.available_quantity = (
            self.quantity - self.reserved_quantity
        )
        super().save(*args, **kwargs)