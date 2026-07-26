# purchases/services.py

from django.db import transaction
from django.utils import timezone

from batches.models import Batch
from inventory.models import Inventory, InventoryTransaction
from .models import Purchase


@transaction.atomic
def receive_purchase(purchase: Purchase):

    if purchase.status == "Received":
        return purchase

    for item in purchase.items.all():

        batch, created = Batch.objects.get_or_create(

            batch_number=item.batch_number,

            defaults={
                "medicine": item.medicine,
                "supplier": purchase.supplier,
                "purchase_date": purchase.purchase_date,
                "expiry_date": item.expiry_date,
                "quantity": item.quantity + item.free_quantity,
                "buying_price": item.unit_cost,
                "selling_price": item.selling_price,
                "status": "Available",
            },
        )

        if not created:
            batch.quantity += (
                item.quantity + item.free_quantity
            )
            batch.buying_price = item.unit_cost
            batch.selling_price = item.selling_price
            batch.save()

        inventory, created = Inventory.objects.get_or_create(

            medicine=item.medicine,
            batch=batch,

            defaults={
                "quantity": item.quantity + item.free_quantity,
                "reserved_quantity": 0,
                "minimum_level": 10,
                "maximum_level": 1000,
                "last_stock_in": timezone.now(),
            },
        )

        if not created:

            inventory.quantity += (
                item.quantity + item.free_quantity
            )

            inventory.last_stock_in = timezone.now()
            inventory.save()

        InventoryTransaction.objects.create(

            medicine=item.medicine,

            batch=batch,

            quantity=item.quantity + item.free_quantity,

            transaction_type="Stock In",

            reference=purchase.purchase_number,

            remarks=f"Purchase {purchase.purchase_number}",

            created_by=purchase.created_by,
        )

        medicine = item.medicine

        medicine.buying_price = item.unit_cost
        medicine.selling_price = item.selling_price

        medicine.save()

    purchase.status = "Received"

    purchase.received_date = timezone.now().date()

    purchase.save()

    return purchase