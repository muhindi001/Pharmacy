from datetime import timedelta

from django.utils import timezone

from batches.models import Batch
from .models import StockAlert


LOW_STOCK_LIMIT = 5
OVERSTOCK_LIMIT = 1000
EXPIRY_DAYS = 30


def sync_stock_alert_for_batch(batch):
    if batch is None or batch.is_deleted:
        return

    low_stock_alert = StockAlert.objects.filter(
        medicine=batch.medicine,
        batch=batch,
        alert_type="Low Stock",
    ).first()

    if batch.remaining_quantity < LOW_STOCK_LIMIT:
        if low_stock_alert:
            low_stock_alert.message = f"Stock level is below {LOW_STOCK_LIMIT} units."
            low_stock_alert.status = "New"
            low_stock_alert.dashboard_notification = True
            low_stock_alert.save(update_fields=["message", "status", "dashboard_notification", "updated_at"])
        else:
            StockAlert.objects.create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Low Stock",
                message=f"Stock level is below {LOW_STOCK_LIMIT} units.",
                status="New",
                dashboard_notification=True,
            )
        return

    if low_stock_alert:
        low_stock_alert.status = "Resolved"
        low_stock_alert.message = f"Stock level recovered to {batch.remaining_quantity} units."
        low_stock_alert.save(update_fields=["status", "message", "updated_at"])


def generate_stock_alerts():

    today = timezone.now().date()

    for batch in Batch.objects.filter(is_deleted=False):
        sync_stock_alert_for_batch(batch)

        if batch.remaining_quantity == 0:
            StockAlert.objects.get_or_create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Out of Stock",
                defaults={
                    "message": "This batch is out of stock."
                }
            )

        elif batch.remaining_quantity >= OVERSTOCK_LIMIT:
            StockAlert.objects.get_or_create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Overstock",
                defaults={
                    "message": "Stock exceeds the configured maximum."
                }
            )

        if batch.expiry_date <= today + timedelta(days=EXPIRY_DAYS):
            StockAlert.objects.get_or_create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Expiry",
                defaults={
                    "message": "Batch expires within the next 30 days."
                }
            )