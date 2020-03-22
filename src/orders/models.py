from django.db import models
from products.models import Product
from django.shortcuts import reverse
from bids.models import Bid

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Order(models.Model):
    uuidcode = models.CharField(max_length=200, unique=True, verbose_name='کد')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ORDER_STATUES = (
        ('created', 'ساخته شده'),
        ('canceled', 'کنسل شده'),
        ('paid', 'پرداخت شده'),
    )
    ORDER_TYPES = (
        ('gateway', 'درگاه پرداخت'),
        ('wallet', 'کیف پول'),
    )

    status = models.CharField(
        max_length=20, default='created', choices=ORDER_STATUES, verbose_name='وضعیت')
    types = models.CharField(
        max_length=20, default='gateway', choices=ORDER_TYPES, verbose_name='نوع پرداخت')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"{self.orders.first()}"

    def get_total_cost(self):
        # items related name hast!!!
        total_cost = sum(item.get_cost() for item in self.orders.all())
        return total_cost

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='orders', on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(
        Product, related_name='orders', on_delete=models.CASCADE, blank=True, null=True, verbose_name='محصول')
    bids = models.ForeignKey(
        Bid, on_delete=models.CASCADE, blank=True, null=True, verbose_name='بید')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    def __str__(self):
        if self.product is not None:
            product_name = self.product.title
        else:
            product_name = ''
        if self.bids is not None:
            bids_name = self.bids.title
        else:
            bids_name = ''
        return f"شماره سفارش { self.order.id }  : {product_name} {bids_name}"

    def get_cost(self):
        return self.price * self.quantity
