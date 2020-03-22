from django.contrib import admin
from .models import Profile, BidBoughts

admin.site.site_header = 'پنل ادمین حراج مارکت (HJM)'


class BidBoughtsAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'product']


admin.site.register(Profile)
admin.site.register(BidBoughts, BidBoughtsAdmin)
