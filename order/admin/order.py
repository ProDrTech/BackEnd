from django.contrib import admin
from ..models import OrderModel, OrderItemModel, PaymentSession
from unfold.admin import ModelAdmin as UnfoldModelAdmin

@admin.register(OrderItemModel)
class OrderItemAdmin(UnfoldModelAdmin):
    """
    Admin Interface for OrderItem
    """
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_at",
    )
    # Faqat OrderItemModel fieldlaridan foydalaning
    search_fields = ('id', )


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 1


@admin.register(OrderModel)
class OrderAdmin(UnfoldModelAdmin):
    """
    Admin Interface for Order
    """
    list_display = (
        "id",
        "name",
        "phone",
        "is_paid",  # ✅ bu yerda to'g'ri ishlatiladi
        "payment_method",
        "delivery_type",
        "created_at",
    )
    list_filter = ('is_paid', 'payment_method', 'delivery_type')
    search_fields = ('id', 'name', 'phone')
    inlines = [OrderItemInline]

@admin.register(PaymentSession)
class PaymentSessionAdmin(UnfoldModelAdmin):
    """
    Admin Interface for PaymentSession
    """
    list_display = (
        "id",
        "user",
        "total_amount",
        "is_paid",
        "created_at",
    )
    list_filter = ("is_paid", "created_at")
    search_fields = ("id", "user__name", "user__user_id", "payme_transaction_id")
    readonly_fields = ("created_at", )

    filter_horizontal = ("orders",) 