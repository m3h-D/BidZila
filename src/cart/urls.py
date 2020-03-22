from django.urls import path
from .views import(
    cart,
    add_to_cart,
    remove_from_cart,
    add_to_bid_cart,
    remove_from_bid_cart,
    bid_cart_view,
    # clear_from_cart,
    # bank_view,
    # get_total_price,
    # clear_cart,
    # add_to_cart_product_list,


)

urlpatterns = [
    path('', cart, name='cart'),
    path('bid-cart/', bid_cart_view, name='bid_cart_view'),
    path('add/<id>/', add_to_cart, name='add_to_cart'),
    path('add-bid/<id>/', add_to_bid_cart, name='add_to_bid_cart'),
    # path('product-list/add/<product_id>/',
    #      add_to_cart_product_list, name='add_to_cart_product_list'),
    path('remove/<id>/', remove_from_bid_cart,
         name='remove_from_bid_cart'),
    path('remove-bid/<product_id>/', remove_from_cart, name='remove_from_cart'),
    # path('clear/<product_id>/', clear_from_cart, name='clear_from_cart'),
    # path('destroy/', clear_cart, name='clear_cart'),
    # path('bank/', bank_view, name='bank'),
    # path('total/', get_total_price, name='total'),
    # path('clearcart/', clear_cart, name='clear_cart'),

]
