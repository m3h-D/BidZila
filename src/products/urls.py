from django.urls import path
from .views import product_detail_view, product_list_view, in_product,  search_view, product_detail_table


urlpatterns = [
    path('list/', product_list_view, name='product_list'),
    path('results/', search_view, name='search'),
    # path('order/', product_ordering, name='ordering'),

    path('category/<slug:cat_slug>/', product_list_view,
         name='product_list_by_category'),
    path('<pk>/<slug>/', product_detail_view, name='product_detail'),
    path('table/<pk>/<slug>/', product_detail_table, name='product_detail_table'),
    path('user/<id>/<slug>/', in_product, name='in_product'),
]
