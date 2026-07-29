from django.db import models
from django.conf import settings

from medicines.models import Medicine
from inventory.models import Inventory

try:
    from batches.models import Batch
except ImportError:
    Batch = None

try:
    from warehouses.models import Warehouse
except ImportError:
    Warehouse = None

try:
    from branches.models import Branch
except ImportError:
    Branch = None


class RFIDReader(models.Model):

    STATUS_CHOICES = (
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
        ("MAINTENANCE", "Maintenance"),
    )

    READER_TYPES = (
        ("HANDHELD", "Handheld"),
        ("FIXED", "Fixed Gate"),
        ("POS", "POS Reader"),
        ("WAREHOUSE", "Warehouse Reader"),
    )

    name = models.CharField(max_length=100)

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    reader_type = models.CharField(
        max_length=20,
        choices=READER_TYPES
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    mac_address = models.CharField(
        max_length=100,
        blank=True
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) if Warehouse else models.CharField(
        max_length=200,
        blank=True
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) if Branch else models.CharField(
        max_length=200,
        blank=True
    )

    location = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ONLINE"
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RFIDTag(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("SOLD", "Sold"),
        ("DAMAGED", "Damaged"),
        ("RETURNED", "Returned"),
        ("LOST", "Lost"),
        ("EXPIRED", "Expired"),
    )

    uid = models.CharField(
        max_length=128,
        unique=True
    )

    epc = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="rfid_tags"
    )

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rfid_tags"
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) if Batch else models.CharField(
        max_length=100,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["uid"]

    def __str__(self):
        return self.uid


class RFIDScan(models.Model):

    SCAN_TYPES = (
        ("RECEIVING", "Receiving"),
        ("SALE", "Sale"),
        ("RETURN", "Return"),
        ("TRANSFER", "Transfer"),
        ("AUDIT", "Audit"),
        ("STOCK_CHECK", "Stock Check"),
    )

    tag = models.ForeignKey(
        RFIDTag,
        on_delete=models.CASCADE,
        related_name="scans"
    )

    reader = models.ForeignKey(
        RFIDReader,
        on_delete=models.SET_NULL,
        null=True,
        related_name="scans"
    )

    scan_type = models.CharField(
        max_length=30,
        choices=SCAN_TYPES
    )

    signal_strength = models.FloatField(
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    scanned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    scanned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-scanned_at"]

    def __str__(self):
        return f"{self.tag.uid} - {self.scan_type}"


class RFIDMovement(models.Model):

    MOVEMENT_TYPES = (
        ("PURCHASE", "Purchase"),
        ("SALE", "Sale"),
        ("TRANSFER", "Transfer"),
        ("RETURN", "Return"),
        ("ADJUSTMENT", "Adjustment"),
        ("AUDIT", "Audit"),
    )

    tag = models.ForeignKey(
        RFIDTag,
        on_delete=models.CASCADE,
        related_name="movements"
    )

    movement_type = models.CharField(
        max_length=30,
        choices=MOVEMENT_TYPES
    )

    from_location = models.CharField(
        max_length=200,
        blank=True
    )

    to_location = models.CharField(
        max_length=200,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    reference = models.CharField(
        max_length=150,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tag.uid} ({self.movement_type})"