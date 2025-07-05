from django.db import models
from django.utils.translation import gettext_lazy as _
from basket.models.basket import CartItemModel
from product.models import ProductModel, ColorModel, SizeModel
from django_core.models import AbstractBaseModel
from users.models import UserModel  



class OrderModel(AbstractBaseModel):
    DELIVERY_CHOICES = [
        ('delivery', _('Dostavka')),
        ('pickup', _('Olib Ketish')),
    ]
    PAYMENT_CHOICES = [
        ('Naqt pul', _('Naqt pul')),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    delivery_type = models.CharField(
        max_length=50,
        choices=DELIVERY_CHOICES,
        default='delivery',
        verbose_name=_('Yetkazib berish turi')
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='cash',
        verbose_name=_("To'lov turi")
    )
    country = models.CharField(max_length=100, verbose_name=_("Viloyat"))
    name = models.CharField(max_length=255, verbose_name=_('Ism'))
    phone = models.CharField(max_length=20, verbose_name=_('Telefon raqam'))
    address = models.TextField(verbose_name=_('Manzil'))
    is_paid = models.BooleanField(default=False, verbose_name=_("To'langanmi?"))  # ✅ Qo‘shildi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqt'))

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.name}"

    class Meta:
        db_table = 'order'
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")



class OrderItemModel(AbstractBaseModel):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items', verbose_name=_("Buyurtma"))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_("Mahsulot"))
    color = models.ForeignKey(ColorModel, on_delete=models.CASCADE, verbose_name=_('Mahsulot rangi'))
    size = models.ForeignKey(SizeModel, on_delete=models.CASCADE, verbose_name=_("Mahsulot o'lchami"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Miqdor"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Narx"))

    @property
    def item_total(self):
        return self.quantity * self.price

    def __int__(self):
        return self.price

    class Meta:
        db_table = 'order_item'
        verbose_name = _("Buyurtma mahsuloti")
        verbose_name_plural = _("Buyurtma mahsulotlari")


class PaymentSession(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name=_("Foydalanuvchi"))
    orders = models.ManyToManyField('order.OrderModel', related_name='payment_sessions', verbose_name=_("Buyurtmalar"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Umumiy summa"))
    is_paid = models.BooleanField(default=False, verbose_name=_("To'langanmi?"))
    payme_transaction_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Payme tranzaksiya ID"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_session'
        verbose_name = _("To'lov sessiyasi")
        verbose_name_plural = _("To'lov sessiyalari")

    def __str__(self):
        return f"{self.user.name} - {self.total_amount} so'm"