from decimal import Decimal
from django.conf import settings

from products.models import Product
from spendations.models import Spend
from django.core import serializers


class Cart(object):

    def __init__(self, request):

        self.session = request.session  # vase har request . session ye session besaz
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # ye 'cart' besaz ba dictunery e khali
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, user, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        product_true_price = str(product.true_price)
        product_new_price = str(product.new_price)
        userspend_f = Spend.objects.filter(user=user, product=product)

        for x in userspend_f:
            if product_id not in self.cart:  # ***
                self.cart[product_id] = {  # product_id alan key e dictunery e cart e ke value hash am baz ye dictunery az quantity o price hast ke in 2 ta ham key haye value haye 0 o product.price an
                    'quantity': 0,
                    'price': str(x.true_price)
                }

        if update_quantity:  # *****
            self.cart[product_id]['quantity'] = quantity
            try:
                product.stack -= quantity - 1
                product.save()
            except:
                pass

        else:
            self.cart[product_id]['quantity'] += quantity
            try:
                product.stack -= quantity
                product.save()
            except:
                pass
        self.save()

    def save(self):
        # in cart i ke ta alan sakhte shude ro beriz to 'cart'
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        try:
            product.stock += self.cart[product_id]['quantity'] - 1
            product.save()
        except:
            pass
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):  # ********
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            # dar dictunary cart ba key e product.id ye value eproduct besaz va tamam e object haye har product o beriz tosh
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
