from payme.views import PaymeWebHookAPIView
from payme.types import response
from payme.models import PaymeTransactions
from order.models.order import PaymentSession
from utils.telegram import send_telegram_message

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def check_perform_transaction(self, params):
        account_id = params['account']['id']
        amount_from_payme = int(params['amount'])

        try:
            session = PaymentSession.objects.get(id=account_id)
        except PaymentSession.DoesNotExist:
            return response.CheckPerformTransaction(error="Order topilmadi").as_resp()

        expected_amount = int(session.total_amount * 100)

        if amount_from_payme != expected_amount:
            return response.CheckPerformTransaction(error="Неверная сумма").as_resp()

        result = response.CheckPerformTransaction(allow=True)
        return result.as_resp()

    def handle_created_payment(self, params, result, *args, **kwargs):
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params['id']
        )
        session = PaymentSession.objects.get(id=transaction.account_id)

        for order in session.orders.all():
            order.is_paid = True
            order.save()

            # ✅ user_id orqali Telegram xabar yuboramiz
            if order.user.user_id:
                send_telegram_message(
                    int(order.user.user_id),
                    "✅ <b>To‘lov qabul qilindi!</b>\nBuyurtmangiz tez orada yetkaziladi."
                )

        session.is_paid = True
        session.save()

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params['id']
        )

        if transaction.state == PaymeTransactions.CANCELED:
            session = PaymentSession.objects.get(id=transaction.account_id)
            session.is_paid = False
            session.save()

            for order in session.orders.all():
                order.is_paid = False
                order.save()

                if order.user.user_id:
                    send_telegram_message(
                        int(order.user.user_id),
                        "❌ <b>To‘lov bekor qilindi.</b>\nIltimos, qaytadan urinib ko‘ring."
                    )
