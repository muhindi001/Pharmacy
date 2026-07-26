from datetime import timedelta

from django.utils import timezone

from batches.models import Batch
from .models import StockAlert


LOW_STOCK_LIMIT = 20
OVERSTOCK_LIMIT = 1000
EXPIRY_DAYS = 30


def generate_stock_alerts():

    today = timezone.now().date()

    for batch in Batch.objects.filter(is_deleted=False):

        if batch.remaining_quantity == 0:
            StockAlert.objects.get_or_create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Out of Stock",
                defaults={
                    "message": "This batch is out of stock."
                }
            )

        elif batch.remaining_quantity <= LOW_STOCK_LIMIT:
            StockAlert.objects.get_or_create(
                medicine=batch.medicine,
                batch=batch,
                alert_type="Low Stock",
                defaults={
                    "message": "Stock level is below the minimum threshold."
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