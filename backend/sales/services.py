from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from .models import Sale, SaleItem
from batches.models import Batch
from inventory.models import InventoryTransaction

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
def get_fefo_batch(medicine, quantity):

    batches = Batch.objects.filter(
        medicine=medicine,
        quantity__gt=0,
        status="Active",
    ).order_by("expiry_date")

    for batch in batches:

        if batch.quantity >= quantity:
            return batch

    return None
@transaction.atomic
def process_sale(validated_data, items):

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

        batch = get_fefo_batch(
            medicine,
            quantity,
        )

        if batch is None:
            raise Exception(
                f"{medicine.medicine_name} is out of stock."
            )

        batch.quantity -= quantity

        batch.save()

        total = quantity * batch.selling_price

        SaleItem.objects.create(
            sale=sale,
            medicine=medicine,
            batch=batch,
            quantity=quantity,
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

    return sale