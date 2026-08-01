from django.db.models.signals import post_save
from django.dispatch import receiver

from batches.models import Batch

from .services import sync_stock_alert_for_batch


@receiver(post_save, sender=Batch)
def batch_stock_alert_signal(sender, instance, **kwargs):
    sync_stock_alert_for_batch(instance)
