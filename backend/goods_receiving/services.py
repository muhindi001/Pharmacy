from django.db import transaction

from batches.models import Batch
from inventory.models import Inventory, InventoryTransaction

from audit.services import AuditService

from .models import GoodsReceipt


class GoodsReceivingService:

    @staticmethod
    @transaction.atomic
    def receive(receipt: GoodsReceipt, user, request=None):

        if receipt.status == "RECEIVED":
            raise ValueError("Goods already received.")

        for item in receipt.items.all():

            batch, created = Batch.objects.get_or_create(
                medicine=item.medicine,
                batch_number=item.batch_number,
                defaults={
                    "manufacturing_date": item.manufacturing_date,
                    "expiry_date": item.expiry_date,
                    "purchase_price": item.purchase_price,
                    "selling_price": item.selling_price,
                },
            )

            inventory, created = Inventory.objects.get_or_create(
                medicine=item.medicine,
                warehouse=receipt.warehouse,
                batch=batch,
                defaults={
                    "quantity": 0,
                    "reserved_quantity": 0,
                    "available_quantity": 0,
                },
            )

            inventory.quantity += item.accepted_quantity
            inventory.available_quantity = (
                inventory.quantity - inventory.reserved_quantity
            )
            inventory.last_stock_in = receipt.received_date
            inventory.last_stock_out = inventory.last_stock_out or None
            inventory.save()

            InventoryTransaction.objects.create(
                batch=batch,
                medicine=item.medicine,
                transaction_type="Stock In",
                quantity=item.accepted_quantity,
                reference_number=receipt.grn_number,
                remarks=f"Goods received {receipt.grn_number}",
                performed_by=user,
            )

            item.inventory_updated = True
            item.save()

        receipt.status = "RECEIVED"
        receipt.save()

        AuditService.log(
            action="GOODS_RECEIVED",
            module="Goods Receiving",
            description=f"{receipt.grn_number} received successfully",
            user=user,
            object_id=receipt.id,
            request=request,
        )

        return receipt