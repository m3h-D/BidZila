from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from products.models import Product
# Create your models here.

User = get_user_model()


class Spend(models.Model):
    user = models.ForeignKey(
        User, related_name='spend', on_delete=models.CASCADE, verbose_name='کاربر')
    user_session = models.CharField(
        max_length=200, null=True, blank=True, verbose_name='کد سشن')
    product = models.ForeignKey(
        Product, related_name='spend', on_delete=models.CASCADE, verbose_name='محصول')

    USER_STATUS = (
        ('winner', 'برنده'),
        ('looser', 'بازنده'),
        ('transferred', 'جایگاه واگذار شده'),
    )

    status = models.CharField(
        max_length=20, blank=True, choices=USER_STATUS, verbose_name='وضعیت')
    user_can = models.BooleanField(default=False, verbose_name='برنده')
    user_ended = models.BooleanField(
        default=False, verbose_name='خریداری کرده')
    user_won = models.BooleanField(
        default=False, verbose_name='ثبت بعنوان برنده اصلی محصول')
    email_send = models.BooleanField(
        default=False, verbose_name='ایمیل فرستاده شده')

    new_price = models.IntegerField(verbose_name='مبلغ کل پیشنهادی')
    # def_offer = models.BooleanField(default=False)
    true_price = models.IntegerField(default=0, verbose_name='قیمت خرید')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='تعداد پیشنهادات داده شده')
    spending = models.IntegerField(
        default=0, verbose_name='مقدار پیشنهادات داده شده')
    last_spend = models.DateTimeField(
        blank=True, verbose_name='زمان اخرین پیشنهاد', default=timezone.now())
    timestamp = models.DateTimeField(
        auto_now=True, verbose_name='زمان اخرین بروزرسانی')
    created = models.DateTimeField(
        default=timezone.now(), verbose_name='اتمام زمان توان خرید')

    def __str__(self):
        return f"{self.user.username}--{self.product.title}"

    class Meta:
        verbose_name = 'شرکت کننده'
        verbose_name_plural = 'شرکت کنندگان'
