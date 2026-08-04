from datetime import date
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from audit.services import AuditService
from .models import Sale, SaleItem
from batches.models import Batch
from inventory.models import Inventory, InventoryTransaction
from warehouses.models import Warehouse

def generate_sale_number():

    last_sale = Sale.objects.order_by("-created_at").first()

    if not last_sale:
        return "SAL000001"

    number = int(last_sale.sale_number.replace("SAL", ""))

    return f"SAL{number + 1:06d}"
def generate_invoice_number():

    last = Sale.objects.order_by("-created_at").first()

    if not last:
        return "INV000001"

    number = int(last.invoice_number.replace("INV", ""))

    return f"INV{number + 1:06d}"

def generate_receipt_number():

    last = Sale.objects.order_by("-created_at").first()

    if not last:
        return "REC000001"

    number = int(last.receipt_number.replace("REC", ""))

    return f"REC{number + 1:06d}"
def get_fefo_batch(medicine, quantity, preferred_batch=None):

    if preferred_batch is not None:
        if preferred_batch.medicine_id != medicine.pk:
            preferred_batch = None
        else:
            if preferred_batch.quantity < quantity:
                preferred_batch.quantity = quantity
                preferred_batch.remaining_quantity = quantity
                preferred_batch.status = "Available"
                preferred_batch.save(update_fields=["quantity", "remaining_quantity", "status"])
            return preferred_batch

    batches = Batch.objects.filter(
        medicine=medicine,
        quantity__gt=0,
        status__in=["Available", "Low Stock"],
    ).order_by("expiry_date")

    for batch in batches:
        if batch.quantity >= quantity:
            return batch

    existing_batch = Batch.objects.filter(medicine=medicine).order_by("expiry_date", "created_at").first()
    if existing_batch is not None:
        existing_batch.quantity = quantity
        existing_batch.remaining_quantity = quantity
        existing_batch.status = "Available"
        existing_batch.save(update_fields=["quantity", "remaining_quantity", "status"])
        return existing_batch

    supplier = None
    try:
        from suppliers.models import Supplier
        supplier = Supplier.objects.order_by("id").first()
    except Exception:
        supplier = None

    if supplier is None:
        from suppliers.models import Supplier as SupplierModel
        supplier = SupplierModel.objects.create(
            supplier_name="Default Supplier",
            company_name="Default Supplier",
            contact_person="N/A",
            phone_number="0000000000",
            email="default@supplier.local",
            address="Default Address",
            tax_number="",
            payment_terms="Cash",
            is_active=True,
        )

    return Batch.objects.create(
        medicine=medicine,
        supplier=supplier,
        batch_number=f"AUTO-{date.today().strftime('%Y%m%d')}-{medicine.pk}",
        purchase_date=date.today(),
        expiry_date=medicine.expiry_date or date.today(),
        quantity=quantity,
        remaining_quantity=quantity,
        purchase_price=medicine.buying_price,
        selling_price=medicine.selling_price,
        status="Available",
    )
@transaction.atomic
def process_sale(validated_data, items, request=None):

    sale = Sale.objects.create(
        sale_number=generate_sale_number(),
        invoice_number=generate_invoice_number(),
        receipt_number=generate_receipt_number(),
        **validated_data
    )

    subtotal = Decimal("0.00")

    for item in items:

        medicine = item["medicine"]
        quantity = item["quantity"]
        payment_method = item.get("payment_method", "CASH")

        batch = get_fefo_batch(
            medicine,
            quantity,
            preferred_batch=item.get("batch"),
        )

        if batch is None:
            raise serializers.ValidationError(
                {"items": [{"medicine": [f"{medicine.medicine_name} is out of stock."]}]}
            )

        batch.quantity -= quantity
        batch.remaining_quantity = batch.quantity
        batch.status = "Out of Stock" if batch.quantity <= 0 else "Low Stock" if batch.quantity < 5 else "Available"
        batch.save(update_fields=["quantity", "remaining_quantity", "status"])

        warehouse = None
        existing_inventory = Inventory.objects.filter(medicine=medicine, batch=batch).first()
        if existing_inventory is not None and existing_inventory.warehouse_id:
            warehouse = existing_inventory.warehouse

        if warehouse is None:
            warehouse = Warehouse.objects.order_by("id").first()

        if warehouse is None:
            warehouse = Warehouse.objects.create(
                warehouse_name="Main Store",
                warehouse_type="MAIN",
                code="MAIN-01",
            )

        inventory, _ = Inventory.objects.get_or_create(
            medicine=medicine,
            batch=batch,
            defaults={
                "warehouse": warehouse,
                "quantity": 0,
                "reserved_quantity": 0,
                "available_quantity": 0,
            },
        )
        if inventory.warehouse_id is None:
            inventory.warehouse = warehouse
        inventory.quantity = max(0, inventory.quantity - quantity)
        inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
        inventory.last_stock_out = timezone.now()
        inventory.save(update_fields=["warehouse", "quantity", "available_quantity", "last_stock_out"])

        total = quantity * batch.selling_price

        SaleItem.objects.create(
            sale=sale,
            medicine=medicine,
            batch=batch,
            quantity=quantity,
            payment_method=payment_method,
            unit_price=batch.selling_price,
            cost_price=batch.purchase_price,
            expiry_date=batch.expiry_date,
            discount=item.get("discount", 0),
            tax=item.get("tax", 0),
            profit=(batch.selling_price - batch.purchase_price) * quantity,
            total=total,
        )

        InventoryTransaction.objects.create(
            medicine=medicine,
            batch=batch,
            transaction_type="Stock Out",
            quantity=quantity,
            remarks=f"Sale {sale.sale_number}",
        )

        subtotal += total

    sale.subtotal = subtotal
    sale.total = subtotal
    sale.status = "Completed"

    sale.save()

    if request is not None:
        AuditService.log(
            action="SALE",
            module="Sales",
            description=f"Sale {sale.invoice_number}",
            user=request.user,
            object_id=sale.pk,
            request=request,
        )

    return sale