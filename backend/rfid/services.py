from django.db import transaction
from django.utils import timezone

from audit.services import AuditService
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

class RFIDScanService:

    @staticmethod
    @transaction.atomic
    def scan_tag(uid, reader_id, scan_type, user, request=None):
        tag = RFIDTag.objects.select_for_update().get(uid=uid)
        reader = RFIDReader.objects.get(pk=reader_id)

        scan = RFIDScan.objects.create(
            tag=tag,
            reader=reader,
            scan_type=scan_type,
            scanned_by=user,
        )

        if request is not None:
            AuditService.log(
                action="RFID_SCAN",
                module="RFID",
                description=f"RFID scanned {tag.uid}",
                user=request.user,
                request=request,
            )

        return scan

class RFIDBulkScanService:

    @staticmethod
    @transaction.atomic
    def bulk_scan(uids, reader_id, scan_type, user, request=None):
        reader = RFIDReader.objects.get(pk=reader_id)
        scans = []

        for uid in uids:
            tag = RFIDTag.objects.select_for_update().get(uid=uid)

            scan = RFIDScan.objects.create(
                tag=tag,
                reader=reader,
                scan_type=scan_type,
                scanned_by=user,
            )
            if request is not None:
                AuditService.log(
                    action="RFID_SCAN",
                    module="RFID",
                    description=f"RFID scanned {tag.uid}",
                    user=request.user,
                    request=request,
                )
            scans.append(scan)

        return scans

class RFIDTransferService:

    @staticmethod
    @transaction.atomic
    def transfer(uid, from_location, to_location):
        tag = RFIDTag.objects.select_for_update().get(uid=uid)

        RFIDMovement.objects.create(
            tag=tag,
            movement_type="TRANSFER",
            from_location=from_location,
            to_location=to_location,
            quantity=tag.quantity,
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