from decimal import Decimal
from django.conf import settings

from bids.models import Bid
from products.models import Product
from django.core import serializers


class BidCart(object):

    def __init__(self, request):

        self.session = request.session  # vase har request . session ye session besaz
        bid_cart = self.session.get(settings.BID_CART_SESSION_ID)
        if not bid_cart:
            # ye 'cart' besaz ba dictunery e khali
            bid_cart = self.session[settings.BID_CART_SESSION_ID] = {}

        self.bid_cart = bid_cart

    def add(self, bid, quantity=1, update_quantity=False):
        bid_id = str(bid.id)
        bid_price = str(bid.price)

        if bid_id not in self.bid_cart:  # ***
            self.bid_cart[bid_id] = {  # product_id alan key e dictunery e cart e ke value hash am baz ye dictunery az quantity o price hast ke in 2 ta ham key haye value haye 0 o product.price an
                'quantity': 0,
                'price': bid_price,
            }

        if update_quantity:  # *****
            self.bid_cart[bid_id]['quantity'] = quantity
            try:
                bid.stack -= quantity - 1
                bid.save()
            except:
                pass

        else:
            self.bid_cart[bid_id]['quantity'] += quantity
            try:
                bid.stack -= quantity
                bid.save()
            except:
                pass
        self.save()

    def save(self):
        # in cart i ke ta alan sakhte shude ro beriz to 'cart'
        self.session[settings.BID_CART_SESSION_ID] = self.bid_cart
        self.session.modified = True

    def remove(self, bid):
        bid_id = str(bid.id)

        try:
            bid.stack += self.bid_cart[bid_id]['quantity'] - 1
            bid.save()
        except:
            pass
        if bid_id in self.bid_cart:
            del self.bid_cart[bid_id]
            self.save()

    def __iter__(self):  # ********
        bid_ids = self.bid_cart.keys()
        bids = Bid.objects.filter(id__in=bid_ids)
        for bid in bids:
            # dar dictunary cart ba key e product.id ye value eproduct besaz va tamam e object haye har product o beriz tosh
            self.bid_cart[str(bid.id)]['bid'] = bid

        for item in self.bid_cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.bid_cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.bid_cart.values())

    def clear(self):
        self.session[settings.BID_CART_SESSION_ID] = {}
        self.session.modified = True
