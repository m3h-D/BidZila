from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'ref_id', 'ref_status', 'amount']


admin.site.register(Payment, PaymentAdmin)
# Register your models here.
