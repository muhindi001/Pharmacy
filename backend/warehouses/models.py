from django.db import models
from medicines.models import Medicine

class Warehouse(models.Model):

    WAREHOUSE_TYPES = (
        ("MAIN", "Main Store"),
        ("BRANCH", "Branch Store"),
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    warehouse_name = models.CharField(
        max_length=150,
        unique=True,
    )

    warehouse_type = models.CharField(
        max_length=20,
        choices=WAREHOUSE_TYPES,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    address = models.TextField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    manager = models.CharField(
        max_length=120,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["warehouse_name"]

    def __str__(self):
        return self.warehouse_name
    
class WarehouseTransfer(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    transfer_number = models.CharField(
        max_length=30,
        unique=True,
    )

    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="transfers_out",
    )

    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="transfers_in",
    )

    transfer_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.transfer_number
    

class WarehouseTransferItem(models.Model):

    transfer = models.ForeignKey(
        WarehouseTransfer,
        on_delete=models.CASCADE,
        related_name="items",
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.medicine.medicine_name