from django.db import models
from django.shortcuts import reverse
# from products.models import Product
# Create your models here.


class Bid(models.Model):
    title = models.CharField(max_length=120, verbose_name='نام')
    slug = models.SlugField(verbose_name='نام نوار ادرس')
    RANK_STATUES = (
        ('gold', 'طلایی'),
        ('silver', 'نقره ای'),
        ('bronze', 'برنزی'),
    )
    rank = models.CharField(max_length=20, default='gold',
                            choices=RANK_STATUES, verbose_name='نوع بید')
    amount = models.PositiveIntegerField(verbose_name='تعداد', default=0)
    stack = models.PositiveIntegerField(verbose_name=' تعداد موجودی')
    secret_key = models.CharField(
        blank=True, max_length=200, verbose_name='کد')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    available = models.BooleanField(default=True, verbose_name='موجود')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    image = models.ImageField(
        blank=True, default='bid.jpg', verbose_name='تصویر')

    created = models.DateTimeField(auto_now_add=True, verbose_name='ساخت پست')
    updated = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی پست')

    class Meta:
        verbose_name = 'بید'
        verbose_name_plural = 'بید ها'

    def __str__(self):
        return f"{ self.title } { self.rank } { self.products.filter(bid_buy=self).first() } ( { self.secret_key} )"

    def get_absolute_url(self):
        return reverse("bids:bid_detail", args=[self.id, self.slug])
