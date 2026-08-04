from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Payment
from .models import Transaction
from .services import TransactionService


@receiver(post_save, sender=Payment)
def create_transaction_after_payment(sender, instance, created, **kwargs):
    """
    Automatically create a transaction when a payment
    becomes SUCCESS.
    """

    if instance.status not in {"SUCCESS", "Paid"}:
        return

    if Transaction.objects.filter(payment=instance).exists():
        return

    TransactionService.create_sale_transaction(instance)