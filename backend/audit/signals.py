from django.db.models.signals import (
    post_save,
    post_delete,
)
from django.dispatch import receiver
from inventory.models import Medicine
from purchases.models import Purchase
from sales.models import Sale
from warehouses.models import WarehouseTransfer

from .models import AuditLog


def system_log(action, module, description):

    AuditLog.objects.create(
        action=action,
        module=module,
        description=description,
    )


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