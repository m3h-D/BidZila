from django.contrib import admin

from .models import Bid


class BidAdmin(admin.ModelAdmin):
    list_display = ['title', 'rank', 'product_name', 'secret_key']

    def product_name(self, obj):
        return obj.products.filter(bid_buy=obj).first()
    product_name.short_description = 'محصول'


admin.site.register(Bid, BidAdmin)

# Register your models here.
