from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session


from products.models import Product
# from products.signals import user_session_signal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.utils import timezone
import datetime


User = get_user_model()
# Create your models here.


class UserSpend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_session = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey(
        Product, related_name='userspend', on_delete=models.CASCADE)
    user_can = models.BooleanField(default=False)
    user_ended = models.BooleanField(default=False)
    email_send = models.BooleanField(default=False)
    user_won = models.BooleanField(default=False)
    new_price = models.IntegerField()
    spending = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now())
    # afk_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-new_price',)

    def __str__(self):
        return f'{self.user.username}'


# class UserSpendItem(models.Model):
#     userspend = models.ForeignKey(
#         UserSpend, related_name='userspenditem', on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, related_name='userspenditem', on_delete=models.CASCADE)
#     new_price = models.IntegerField(default=0)
#     spending = models.IntegerField(default=0)

#     class Meta:
#         ordering = ('-spending',)

#     def __str__(self):
#         return f'{self.userspend.user.username}--{self.product}'


class UserSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    user_session = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='کد سشن')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='زمان اخرین تغییرات')
    # time_can = models.DateTimeField(blank=True, default=timezone.now(), verbose_name='')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "سشن کاربر"
        verbose_name_plural = "سشن کاربران"


user_session_signal = Signal(providing_args=['instance', 'request'])


def user_session_reciver(sender, instance, request, *args, **kwargs):
    user = instance
    session_key = request.session.session_key
    UserSession.objects.update_or_create(user=user, user_session=session_key)


user_session_signal.connect(user_session_reciver)


class UserWinner(models.Model):
    user = models.ForeignKey(
        User, related_name='userwinner', on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(
        Product, related_name='userwinner', on_delete=models.CASCADE, verbose_name="محصول")
    new_price = models.IntegerField(verbose_name="مبلغ کل پیشنهادی")
    spending = models.IntegerField(
        default=0, verbose_name="مقدار پیشنهاد داده شده")
    offered = models.SmallIntegerField(
        default=0, verbose_name="درصد تخفیف")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخت این ردیف")
    timestamp = models.DateTimeField(
        auto_now=True, verbose_name="زمان اخرین بروزرسانی")

    class Meta:
        verbose_name = "کاربر برنده"
        verbose_name_plural = "کاربران برنده شده"

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.product.title)
