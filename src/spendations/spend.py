from decimal import Decimal
from django.conf import settings

from products.models import Product


class Spend(object):
    def __init__(self,  request):
        self.session = request.session
        spend = self.session.get(settings.SPEND_SESSION_ID)
        if not spend:
            spend = self.session[settings.SPEND_SESSION_ID] = {}

        self.spend = spend

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.spend:
            self.spend[product_id] = {
                'new_price': str(product.new_price),
                'can_spend': str(product.can_spend),
                'quantity': 0,

            }
        if update_quantity:
            self.spend[product_id]['quantity'] = quantity
        else:
            self.spend[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.SPEND_SESSION_ID] = self.spend
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.spend:
            del self.spend[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.spend.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.spend[str(product.id)]['product'] = product

        for item in self.spend.values():
            item['can_spend'] = Decimal(item['can_spend'])
            item['new_price'] = Decimal(item['new_price'])
            item['spending'] = item['can_spend'] * item['quantity']
            item['new_price'] += item['spending']
            yield item

    def get_total_spend(self):
        return sum(Decimal(item['can_spend']) * item['quantity'] for item in self.spend.values())

    def clear(self):
        self.session[settings.SPEND_SESSION_ID] = {}
        self.session.modified = True
