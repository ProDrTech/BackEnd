# services/payment.py
from order.models import OrderModel, PaymentSession
from django.conf import settings
from decimal import Decimal

def create_payment_session(user):
    orders = OrderModel.objects.filter(user=user, is_paid=False)
    
    if not orders.exists():
        return None 

    total = sum([
        sum([item.item_total for item in order.order_items.all()])
        for order in orders
    ], Decimal(0)) 

    session = PaymentSession.objects.create(
        user=user,
        total_amount=total
    )
    
    session.orders.set(orders)

    return session