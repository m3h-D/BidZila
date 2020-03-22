import csv
import datetime

from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse

from .models import Order, OrderItem
from payments.models import Payment
from accounts.models import Profile
# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields(
    ) if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Excel'


# class ProfileOrderInline(admin.StackedInline):
#     model = Profile
#     autocomplete_fields = ('user',)
#     extra = 0


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    # bayraye inke in inja kar kone, bayad tu Schedule search filedesh kar kone!
    autocomplete_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = (
        'uuidcode', 'paid', 'orderphone', 'orderuser', 'status', 'jcreated', 'payment_ref_id', 'order_detail',
    )
    search_fields = ('id', 'user__first_name', 'user__last_name')

    def orderuser(self, obj):
        return f"{obj.user.profile.first_name} {obj.user.profile.last_name}"
    orderuser.short_description = 'نام و نام خانوادگی'

    def orderphone(self, obj):
        return f'{obj.user.profile.phone}'
    orderphone.short_description = "تلفن"
    # admin order(sort) on fk (calculated fields)

    def jcreated(self, obj):
        # return obj.exam_date
        gy = obj.created.year
        gm = obj.created.month
        gd = obj.created.day
        # print(dir(obj.created))
        jlist = gregorian_to_jalali(gy, gm, gd)  # list
        # return f'{jlist[0]}/{jlist[1]}/{jlist[2]} - {obj.created.hour}:{obj.created.minute}'
        return f'{jlist[0]}/{jlist[1]}/{jlist[2]}'
    jcreated.short_description = "تاریخ"

    def payment_ref_id(self, obj):
        payment_obj = Payment.objects.filter(order_id=obj.id)
        for x in payment_obj:
            if not x.ref_id:
                return f'ندارد'
            return f'{x.ref_id}'
    payment_ref_id.short_description = "پیگیری"

    def get_products(self, obj):
        return ",".join([str(product) for product in obj.orderitem.product.all()])

    get_products.short_description = " محصولات "

    def order_detail(self, obj):

        return mark_safe('<a href="{}">نمایش</a>'.format(reverse('orders:order_detail', args=[obj.id])))

    order_detail.short_description = "جزییات"

    inlines = (OrderItemInline,)
    actions = [export_to_csv]


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if(gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if(gm > 2):
        gy2 = gy+1
    else:
        gy2 = gy
    days = (365*gy) + (int((gy2+3)/4)) - (int((gy2+99)/100)) + \
        (int((gy2+399)/400)) - 80 + gd + g_d_m[gm-1]
    jy += 33*(int(days/12053))
    days %= 12053
    jy += 4*(int(days/1461))
    days %= 1461
    if(days > 365):
        jy += int((days-1)/365)
        days = (days-1) % 365
    if(days < 186):
        jm = 1+int(days/31)
        jd = 1+(days % 31)
    else:
        jm = 7+int((days-186)/30)
        jd = 1+((days-186) % 30)
    return [jy, jm, jd]


# admin.site.register(Order)
# admin.site.register(OrderItem)
