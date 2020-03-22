from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator

from products.models import Product
from bids.models import Bid


User = get_user_model()


class BidBoughts(models.Model):
    user = models.ForeignKey(
        User, related_name='bidboughts', on_delete=models.CASCADE, verbose_name='کاربر')
    bid = models.ForeignKey(Bid,  on_delete=models.CASCADE, verbose_name='بید')
    product = models.ForeignKey(
        Product, related_name='bidboughts', default=1, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField(max_length=120, verbose_name='نام')
    secret_key = models.CharField(
        default='', max_length=200, verbose_name='کد')
    amount = models.IntegerField(default=0, verbose_name='تعداد بیدها')
    ended = models.BooleanField(default=False, verbose_name='اتمام بید')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'بید خریداری شده'
        verbose_name_plural = 'بیدهای خریداری شده'

    def __str__(self):
        return f"{self.user.username}--{ self.product.title }--{self.title}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name='نام کاربری')
    first_name = models.CharField(
        max_length=120, blank=True, verbose_name='نام', null=True)
    last_name = models.CharField(
        max_length=120, blank=True, verbose_name='نام خانوادگی', null=True)
    bio = models.CharField(max_length=500, blank=True,
                           verbose_name='درباره من')
    city = models.CharField(max_length=30, blank=True, verbose_name='شهر')
    address = models.CharField(
        max_length=1000, blank=True, verbose_name='ادرس')
    phone_reg = RegexValidator(
        regex=r'[0][9][0-9]{9,9}$')
    phone = models.CharField(
        validators=[phone_reg], max_length=11, null=True, verbose_name='شماره تلفن')

    post_code = models.CharField(
        max_length=20, blank=True, verbose_name='کدپستی')
    image = models.ImageField(default='default.jpg',
                              blank=True, verbose_name='اواتار')
    score = models.PositiveIntegerField(default=0, verbose_name='امتیاز')
    wallet = models.PositiveIntegerField(default=0, verbose_name='کیف پول')
    # have_bid = models.ManyToManyField(
    #     BidBoughts, related_name='profile',  verbose_name='تعداد بید ها', blank=True)

    def __str__(self):
        return f'پروفایل : {self.user.username}'

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
