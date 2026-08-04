from invoices.models import Invoice, Receipt
from transactions.services import TransactionService


def finalize_payment(payment):
    payment.status = "SUCCESS"
    payment.save(update_fields=["status"])

    transaction = TransactionService.create_sale_transaction(payment)

    sale = payment.sale
    if sale and not hasattr(sale, "invoice"):
        invoice_number = f"INV-{sale.invoice_number or sale.sale_number or payment.payment_number}"
        Invoice.objects.create(
            invoice_number=invoice_number,
            sale=sale,
            customer=payment.customer,
            payment=payment,
            subtotal=sale.subtotal or payment.amount or 0,
            discount=sale.discount or 0,
            tax=sale.tax or 0,
            total=sale.total or payment.amount or 0,
            status="Paid",
        )

    if sale and hasattr(sale, "invoice") and sale.invoice:
        Receipt.objects.create(
            receipt_number=f"REC-{payment.payment_number or sale.receipt_number or sale.sale_number}",
            invoice=sale.invoice,
            payment=payment,
            cashier=payment.cashier,
            payment_method=payment.payment_method,
            amount_paid=payment.amount_paid or payment.amount or 0,
            balance=payment.balance or 0,
        )

    return transaction
