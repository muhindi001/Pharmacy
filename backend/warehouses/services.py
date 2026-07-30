from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from inventory.models import Inventory, InventoryTransaction

from .models import (
    Warehouse,
    WarehouseTransfer,
    WarehouseTransferItem,
)

class WarehouseService:

    @staticmethod
    def create_warehouse(**data):
        return Warehouse.objects.create(**data)

    @staticmethod
    def update_warehouse(instance, **data):

        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @staticmethod
    def warehouse_summary(warehouse):

        inventory = Inventory.objects.filter(
            warehouse=warehouse
        )

        total_products = inventory.count()

        total_quantity = (
            inventory.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )

        return {
            "warehouse": warehouse.warehouse_name,
            "products": total_products,
            "quantity": total_quantity,
        }
        
class WarehouseTransferService:

    @staticmethod
    @transaction.atomic
    def create_transfer(
        transfer_number,
        from_warehouse,
        to_warehouse,
        items,
    ):

        if from_warehouse == to_warehouse:
            raise ValueError(
                "Source and destination warehouse cannot be the same."
            )

        transfer = WarehouseTransfer.objects.create(
            transfer_number=transfer_number,
            from_warehouse=from_warehouse,
            to_warehouse=to_warehouse,
            transfer_date=timezone.now().date(),
        )

        for item in items:

            WarehouseTransferItem.objects.create(
                transfer=transfer,
                medicine=item["medicine"],
                quantity=item["quantity"],
            )

        return transfer

    @staticmethod
    def approve_transfer(transfer):

        transfer.status = "APPROVED"
        transfer.save()

        return transfer
    
    @staticmethod
    @transaction.atomic
    def complete_transfer(transfer):

        if transfer.status == "COMPLETED":
            return transfer

        for item in transfer.items.all():

            source = Inventory.objects.select_for_update().get(
                warehouse=transfer.from_warehouse,
                medicine=item.medicine,
            )

            if source.quantity < item.quantity:
                raise ValueError(
                    f"Insufficient stock for {item.medicine}"
                )

            source.quantity -= item.quantity
            source.save()

            destination, created = Inventory.objects.get_or_create(
                warehouse=transfer.to_warehouse,
                medicine=item.medicine,
                defaults={
                    "quantity": 0
                },
            )

            destination.quantity += item.quantity
            destination.save()
            
            InventoryTransaction.objects.create(
                inventory=source,
                transaction_type="TRANSFER_OUT",
                quantity=item.quantity,
                reference=transfer.transfer_number,
            )

            InventoryTransaction.objects.create(
                inventory=destination,
                transaction_type="TRANSFER_IN",
                quantity=item.quantity,
                reference=transfer.transfer_number,
            )

        transfer.status = "COMPLETED"
        transfer.save()

        return transfer
    
    @staticmethod
    def cancel_transfer(transfer):

        transfer.status = "CANCELLED"
        transfer.save()

        return transfer
class WarehouseInventoryService:

    @staticmethod
    @transaction.atomic
    def receive_stock(
        warehouse,
        medicine,
        quantity,
    ):

        inventory, created = Inventory.objects.get_or_create(
            warehouse=warehouse,
            medicine=medicine,
            defaults={
                "quantity": 0
            },
        )

        inventory.quantity += quantity
        inventory.save()

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="PURCHASE",
            quantity=quantity,
            reference="GOODS RECEIVED",
        )

        return inventory
    @staticmethod
    @transaction.atomic
    def remove_stock(
        warehouse,
        medicine,
        quantity,
    ):

        inventory = Inventory.objects.select_for_update().get(
            warehouse=warehouse,
            medicine=medicine,
        )

        if inventory.quantity < quantity:
            raise ValueError(
                "Insufficient stock."
            )

        inventory.quantity -= quantity
        inventory.save()

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="SALE",
            quantity=quantity,
            reference="POS SALE",
        )

        return inventory
    @staticmethod
    @transaction.atomic
    def adjust_stock(
        warehouse,
        medicine,
        quantity,
        reason,
    ):

        inventory = Inventory.objects.select_for_update().get(
            warehouse=warehouse,
            medicine=medicine,
        )

        inventory.quantity += quantity
        inventory.save()

        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type="ADJUSTMENT",
            quantity=quantity,
            reference=reason,
        )

        return inventory
class WarehouseReportService:

    @staticmethod
    def stock_by_warehouse(warehouse):

        return Inventory.objects.filter(
            warehouse=warehouse
        ).select_related(
            "medicine"
        )

    @staticmethod
    def low_stock(warehouse):

        return Inventory.objects.filter(
            warehouse=warehouse,
            quantity__lte=10,
        )

    @staticmethod
    def total_stock_value(warehouse):

        inventory = Inventory.objects.filter(
            warehouse=warehouse
        )

        total = 0

        for item in inventory:
            total += item.quantity * item.medicine.selling_price

        return total
