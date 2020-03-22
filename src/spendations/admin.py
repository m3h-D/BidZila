from django.contrib import admin
from .models import Spend


class SpendAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_can',
                    'product', 'new_price', 'user_session', 'last_spend']


admin.site.register(Spend, SpendAdmin)

# Register your models here.
