from django.contrib import admin
from .models import Product, Category, CanSpend
from userspends.models import UserWinner

admin.site.register(CanSpend)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class UserWinnerInline(admin.StackedInline):
    model = UserWinner
    # bayraye inke in inja kar kone, bayad tu Schedule search filedesh kar kone!
    autocomplete_fields = ['product']
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'available', 'event', 'ended', 'out_of_user', 'event_start', 'event_end', 'category', 'new_price', 'true_price',
                    'stack', 'created', 'id', ]
    # har field i ke in ja hast bayad to list_displaye ham bashe
    list_filter = ['created', 'category']
    list_editable = ['new_price', 'stack',
                     'event_start', 'available', 'event_end', 'category']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('id', 'title', 'category')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'true_price', 'new_price', 'stack', 'event_start', 'event_end', 'bid_buy', 'can_spend', 'image', 'image2', 'image3', 'reset')
        }),
        ('پیشرفته', {
            'classes': ('collapse',),
            'fields': ('slug', 'final_price', 'precent_price', 'out_of_user', 'available', 'special', 'event', 'ended', 'secret_key', 'user', 'user_session', 'cannot_buy'),
        }),

    )
    inlines = (UserWinnerInline,)


admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductComment)
