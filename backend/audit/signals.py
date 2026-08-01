from django.db.models.signals import (
    post_save,
    post_delete,
)
from django.dispatch import receiver

from batches.models import Batch
from categories.models import Category
from customers.models import Customer
from inventory.models import Inventory
from medicines.models import Medicine
from purchases.models import Purchase
from sales.models import Sale
from suppliers.models import Supplier
from warehouses.models import WarehouseTransfer

from .models import AuditLog


def system_log(action, module, description):

    AuditLog.objects.create(
        action=action,
        module=module,
        description=description,
    )


# ===========================================================
# Category
# ===========================================================

@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, **kwargs):
    if created:
        system_log("CREATE", "Category", f"Category created: {instance.category_name}")
    else:
        system_log("UPDATE", "Category", f"Category updated: {instance.category_name}")


# ===========================================================
# Supplier
# ===========================================================

@receiver(post_save, sender=Supplier)
def supplier_saved(sender, instance, created, **kwargs):
    if created:
        system_log("CREATE", "Supplier", f"Supplier created: {instance.supplier_name}")
    else:
        system_log("UPDATE", "Supplier", f"Supplier updated: {instance.supplier_name}")


# ===========================================================
# Customer
# ===========================================================

@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, created, **kwargs):
    if created:
        system_log("CREATE", "Customer", f"Customer created: {instance.customer_code}")
    else:
        system_log("UPDATE", "Customer", f"Customer updated: {instance.customer_code}")


# ===========================================================
# Medicine
# ===========================================================

@receiver(post_save, sender=Medicine)
def medicine_saved(sender, instance, created, **kwargs):

    if created:

        system_log(
            "CREATE",
            "Medicine",
            f"Medicine created: {instance.medicine_name}",
        )

    else:

        system_log(
            "UPDATE",
            "Medicine",
            f"Medicine updated: {instance.medicine_name}",
        )


@receiver(post_delete, sender=Medicine)
def medicine_deleted(sender, instance, **kwargs):

    system_log(
        "DELETE",
        "Medicine",
        f"Medicine deleted: {instance.medicine_name}",
    )


# ===========================================================
# Batch
# ===========================================================

@receiver(post_save, sender=Batch)
def batch_saved(sender, instance, created, **kwargs):
    if created:
        system_log("CREATE", "Batch", f"Batch created: {instance.batch_number}")
    else:
        system_log("UPDATE", "Batch", f"Batch updated: {instance.batch_number}")


# ===========================================================
# Inventory
# ===========================================================

@receiver(post_save, sender=Inventory)
def inventory_saved(sender, instance, created, **kwargs):
    if created:
        system_log("CREATE", "Inventory", f"Inventory created: {instance.medicine.medicine_name}")
    else:
        system_log("UPDATE", "Inventory", f"Inventory updated: {instance.medicine.medicine_name}")


# ===========================================================
# Purchase
# ===========================================================

@receiver(post_save, sender=Purchase)
def purchase_saved(sender, instance, created, **kwargs):

    if created:

        system_log(
            "PURCHASE",
            "Purchase",
            f"Purchase {instance.purchase_number} created",
        )

    elif instance.status == "Received":

        system_log(
            "RECEIVED",
            "Purchase",
            f"Purchase received: {instance.purchase_number}",
        )

    else:

        system_log(
            "UPDATE",
            "Purchase",
            f"Purchase {instance.purchase_number} updated",
        )


# ===========================================================
# Sale
# ===========================================================

@receiver(post_save, sender=Sale)
def sale_saved(sender, instance, created, **kwargs):

    if created:

        system_log(
            "SALE",
            "Sales",
            f"Sale {instance.invoice_number} created",
        )

    elif instance.status == "Completed":

        system_log(
            "COMPLETED",
            "Sales",
            f"Sale completed: {instance.invoice_number}",
        )

    else:

        system_log(
            "UPDATE",
            "Sales",
            f"Sale {instance.invoice_number} updated",
        )


# ===========================================================
# Warehouse Transfer
# ===========================================================

@receiver(post_save, sender=WarehouseTransfer)
def warehouse_transfer_saved(sender, instance, created, **kwargs):

    if created:

        system_log(
            "TRANSFER",
            "Warehouse",
            f"Transfer {instance.transfer_number} created",
        )

    else:

        system_log(
            "UPDATE",
            "Warehouse",
            f"Transfer {instance.transfer_number} updated",
        )