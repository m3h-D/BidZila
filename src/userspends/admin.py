from django.contrib import admin
from .models import UserSession, UserWinner


class UserSpendAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_can',
                    'product', 'new_price', 'user_session', ]


class UserWarningAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'new_price']


# admin.site.register(UserSpend, UserSpendAdmin)
admin.site.register(UserSession)
admin.site.register(UserWinner, UserWarningAdmin)
# admin.site.register(UserSpendItem)  # , UserSpendItemAdmin)
# Register your models here.
