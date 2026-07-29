from django.db import transaction
from django.utils import timezone

from inventory.models import Inventory
from inventory.models import InventoryTransaction

from .models import (
    RFIDTag,
    RFIDReader,
    RFIDScan,
    RFIDMovement,
)

class RFIDTagService:

    @staticmethod
    def register_tag(
        medicine,
        inventory,
        uid,
        batch=None,
        quantity=1,
    ):

        return RFIDTag.objects.create(
            uid=uid,
            medicine=medicine,
            inventory=inventory,
            batch=batch,
            quantity=quantity,
        )
        
class RFIDReturnService:

    @staticmethod
    @transaction.atomic
    def return_item(uid):

        tag = RFIDTag.objects.select_for_update().get(
            uid=uid
        )

        inventory = tag.inventory

        inventory.quantity += 1
        inventory.save()

        tag.status = "RETURNED"
        tag.save(update_fields=["status"])

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="RETURN",
            quantity=1,
            reference=uid,
        )

        RFIDMovement.objects.create(
            tag=tag,
            movement_type="RETURN",
            quantity=1,
            reference=uid,
        )

        return tag

class RFIDReceivingService:

    @staticmethod
    @transaction.atomic
    def receive(uid, qty=1):

        tag = RFIDTag.objects.select_for_update().get(
            uid=uid
        )

        inventory = tag.inventory

        inventory.quantity += qty
        inventory.save()

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="PURCHASE",
            quantity=qty,
            reference=uid,
        )

        RFIDMovement.objects.create(
            tag=tag,
            movement_type="PURCHASE",
            to_location="Warehouse",
            quantity=qty,
            reference=uid,
        )

        return inventory
    
class RFIDSaleService:

    @staticmethod
    @transaction.atomic
    def sell(uid):

        tag = RFIDTag.objects.select_for_update().get(
            uid=uid
        )

        inventory = tag.inventory

        if inventory.quantity <= 0:
            raise ValueError(
                "Medicine out of stock."
            )

        inventory.quantity -= 1
        inventory.save()

        tag.status = "SOLD"
        tag.save(update_fields=["status"])

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="SALE",
            quantity=1,
            reference=uid,
        )

        RFIDMovement.objects.create(
            tag=tag,
            movement_type="SALE",
            quantity=1,
            reference=uid,
        )

        return tag
class RFIDReturnService:

    @staticmethod
    @transaction.atomic
    def return_item(uid):

        tag = RFIDTag.objects.select_for_update().get(
            uid=uid
        )

        inventory = tag.inventory

        inventory.quantity += 1
        inventory.save()

        tag.status = "RETURNED"
        tag.save(update_fields=["status"])

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="RETURN",
            quantity=1,
            reference=uid,
        )

        RFIDMovement.objects.create(
            tag=tag,
            movement_type="RETURN",
            quantity=1,
            reference=uid,
        )

        return tag
    
class RFIDAuditService:

    @staticmethod
    def audit(scanned_uids):

        database_uids = set(
            RFIDTag.objects.filter(
                status="ACTIVE"
            ).values_list(
                "uid",
                flat=True,
            )
        )

        scanned = set(scanned_uids)

        return {
            "expected": len(database_uids),
            "scanned": len(scanned),
            "missing": list(database_uids - scanned),
            "unexpected": list(scanned - database_uids),
        }