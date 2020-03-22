from django.db import models
from django.contrib.auth import get_user_model

from orders.models import Order

User = get_user_model()
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='سفارش')
    ref_id = models.CharField(max_length=200, verbose_name='ایدی درگاه پرداخت')
    ref_status = models.CharField(
        max_length=200, verbose_name='وضعیت درگاه پرداخت')
    amount = models.PositiveIntegerField(
        default=0, verbose_name='مبلغ پرداختی')

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'
