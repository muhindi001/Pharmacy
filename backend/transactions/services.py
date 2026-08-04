from .models import Transaction


class TransactionService:

    @staticmethod
    def create_sale_transaction(payment):

        if payment.status != "SUCCESS":
            return None

        transaction = Transaction.objects.create(

            sale=payment.sale,

            payment=payment,

            customer=payment.sale.customer,

            cashier=getattr(payment, "cashier", None),

            transaction_type="SALE",

            payment_method=payment.payment_method,

            amount=payment.amount,

            reference_number=getattr(
                payment,
                "reference_number",
                "",
            ),

            description=(
                f"Payment received for "
                f"Sale {payment.sale.id}"
            ),

            status="SUCCESS",
        )

        return transaction

    @staticmethod
    def create_refund_transaction(refund):

        transaction = Transaction.objects.create(

            sale=refund.sale,

            customer=refund.sale.customer,

            cashier=getattr(refund, "cashier", None),

            transaction_type="REFUND",

            payment_method=refund.payment_method,

            amount=refund.amount,

            reference_number=refund.reference_number,

            description="Customer Refund",

            status="SUCCESS",
        )

        return transaction

    @staticmethod
    def create_purchase_transaction(receiving):

        transaction = Transaction.objects.create(

            transaction_type="PURCHASE",

            payment_method="BANK",

            amount=receiving.total_amount,

            reference_number=receiving.receiving_number,

            description="Goods Receiving",

            status="SUCCESS",
        )

        return transaction