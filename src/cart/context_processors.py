from .cart import Cart
from .bidcart import BidCart


def cart(request):
    if 'bid-cart' in request.META['PATH_INFO'] or 'bankbid' in request.META['PATH_INFO']:
        return {}
    else:
        return {'cart': Cart(request)}


def bid_cart(request):
    if 'cart' in request.META['PATH_INFO'] or 'bank' in request.META['PATH_INFO']:
        return {}
    else:
        return {'bid_cart': BidCart(request)}
