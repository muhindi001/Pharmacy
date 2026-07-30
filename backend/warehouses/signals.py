from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models import (
    Inventory,
    InventoryTransaction,
)

from .models import (
    WarehouseTransfer,
)
@receiver(post_save, sender=WarehouseTransfer)
def process_completed_transfer(sender, instance, created, **kwargs):

    if instance.status != "COMPLETED":
        return

    if getattr(instance, "_inventory_processed", False):
        return

    instance._inventory_processed = True

    with transaction.atomic():

        for item in instance.items.select_related("medicine"):

            source = Inventory.objects.select_for_update().get(
                warehouse=instance.from_warehouse,
                medicine=item.medicine,
            )

            if source.quantity < item.quantity:
                raise ValueError(
                    f"Insufficient stock for {item.medicine}"
                )

            source.quantity -= item.quantity
            source.save()

            destination, created = Inventory.objects.get_or_create(
                warehouse=instance.to_warehouse,
                medicine=item.medicine,
                defaults={
                    "quantity": 0,
                },
            )

            destination.quantity += item.quantity
            destination.save()

            InventoryTransaction.objects.create(
                inventory=source,
                transaction_type="TRANSFER_OUT",
                quantity=item.quantity,
                reference=instance.transfer_number,
            )

            InventoryTransaction.objects.create(
                inventory=destination,
                transaction_type="TRANSFER_IN",
                quantity=item.quantity,
                reference=instance.transfer_number,
            )