from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.utils import timezone
from bids.models import Bid


User = get_user_model()

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'کتگوری'
        verbose_name_plural = 'کتگوری ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class CanSpend(models.Model):
    title = models.CharField(max_length=100,  default='')
    spend = models.IntegerField(default=0, verbose_name='مبلغ پیشنهادی')
    mult = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'مبلغ پیشنهاد'
        verbose_name_plural = 'مبلغ پیشنهاد'

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    # id = models.AutoField(
    #     auto_created=True, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=120, verbose_name='نام محصول')
    slug = models.SlugField(
        max_length=200, db_index=True, verbose_name='مستعار')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='دسته')
    description = models.TextField(verbose_name='توضیحات')
    true_price = models.IntegerField(default=0, verbose_name='قیمت بازار')
    new_price = models.IntegerField(default=0, verbose_name='قیمت کف')
    final_price = models.IntegerField(default=0, verbose_name='قیمت تمام شده')

    precent_price = models.IntegerField(verbose_name='30% قیمت', blank=True)
    out_of_user = models.BooleanField(
        default=False, verbose_name='غیرقابل شرکت')
    stack = models.PositiveIntegerField(verbose_name='تعداد')
    available = models.BooleanField(default=True, verbose_name='دردسترس')
    special = models.BooleanField(default=False, verbose_name='پیشنهاد ویژه')

    reset = models.BooleanField(
        default=False, verbose_name='انتخاب دوباره برای حراجی')
    event_start = models.DateTimeField(verbose_name='شروع حراجی')
    event_end = models.DateTimeField(verbose_name='پایان حراجی')
    event = models.BooleanField(default=False, verbose_name='حراجی')
    secret_key = models.CharField(
        blank=True, max_length=200, verbose_name='کد')
    bid_buy = models.ManyToManyField(Bid, related_name='products')
    user = models.ManyToManyField(
        User, related_name='product', blank=True, verbose_name='شرکت کنندگان')
    user_session = models.CharField(
        max_length=200, null=True, blank=True, verbose_name='کد خرید')

    # time_end = models.DateTimeField(blank=True)
    ended = models.BooleanField(default=False, verbose_name='پایان حراجی')
    cannot_buy = models.BooleanField(
        default=False, verbose_name='پایان زمان برای خرید محصول')

    can_spend = models.ForeignKey(
        CanSpend, on_delete=models.CASCADE, blank=True, verbose_name='قیمت پیشنهادی')

    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخت پست')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی پست')

    image = models.ImageField(blank=False, default='product.jpg')
    image2 = models.ImageField(blank=True, null=True, default='product.jpg')
    image3 = models.ImageField(blank=True, null=True, default='product.jpg')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    def get_user_url(self):
        return reverse('products:in_product', args=[self.id, self.slug])


# def event_signal_reciver(sender, instance, request, *args, **kwargs):
#     product = instance

#     Product.objects.update(event_end=product, event=True)


# event_signal.connect(event_signal_reciver)
