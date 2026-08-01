from django.db.models.signals import post_save
from django.dispatch import receiver

from audit.services import AuditService

from .models import GoodsReceipt


@receiver(post_save, sender=GoodsReceipt)
def goods_receipt_created(sender, instance, created, **kwargs):

    if created:

        AuditService.log(
            action="CREATE",
            module="Goods Receiving",
            description=f"Created GRN {instance.grn_number}",
            user=instance.received_by,
            object_id=instance.pk,
        )


@receiver(post_save, sender=GoodsReceipt)
def goods_receipt_received(sender, instance, created, **kwargs):

    if not created and instance.status == "RECEIVED":

        AuditService.log(
            action="RECEIVED",
            module="Goods Receiving",
            description=f"Received GRN {instance.grn_number}",
            user=instance.received_by,
            object_id=instance.pk,
        )