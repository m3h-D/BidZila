from django.urls import path
from .views import order_detail, order_created, orders, bid_order_created, wallet_order_create, bid_order_Wallet_created

urlpatterns = [
    path('list/', orders, name='order_list'),
    path('detail/<id>/', order_detail, name='order_detail'),
    path('bank/', order_created, name='bank'),
    path('bankbid/', bid_order_created, name='bank2'),
    path('bank-wallet/', wallet_order_create, name='bank3'),
    path('bankbid-wallet/', bid_order_Wallet_created, name='bank4'),
]
