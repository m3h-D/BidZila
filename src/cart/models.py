# from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save, pre_save, m2m_changed
# from django.contrib.auth.models import User

# from products.models import Product
# from decimal import Decimal

# class CartManager(models.Manager):
#     def new_or_get(self, request):
#         cart_id = request.session.get('cart_id', None)
#         qs = self.get_queryset().filter(id=cart_id)
#         if qs.count() == 1:
#             new_obj = False
#             cart = qs.first()
#             #  fek konam beshe if e paein o hazf kard
#             if request.user.is_authenticated and cart.user is None:
#                 cart.user = request.user
#                 cart.save()
#         else:
#             cart = Cart.objects.create(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart.id
#         return cart, new_obj


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ManyToManyField(Product, blank=True)
#     total = models.DecimalField(
#         max_digits=100000, decimal_places=0, default=0)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)

#     # objects = CartManager()

#     def __str__(self):
#         return f'{self.user.username} -- با شماره کارت :  {self.id}'

#     def add_to_cart(self, product_id):
#         product = Product.objects.get(id=product_id)
#         try:  # age un product to cart bud yedoone be quantity ezaf kon
#             exist_order = CartItem.objects.get(product=product, cart=self)
#             exist_order.quantity += 1

#             exist_order.save()
#         except CartItem.DoesNotExist:  # ye cart jadid besaz product o beriz to un
#             new_order = CartItem.objects.create(
#                 product=product,
#                 cart=self,
#                 quantity=1,
#             )
#             new_order.save()

#     def remove_from_cart(self, product_id):
#         product = Product.objects.get(pk=product_id)
#         try:
#             exist_order = CartItem.objects.get(product=product, cart=self)

#             if exist_order.quantity > 1:
#                 exist_order.quantity -= 1
#                 exist_order.save()
#             else:
#                 exist_order.delete()

#         except CartItem.DoesNotExist:
#             pass

#     def clear_from_cart(self, product_id):
#         product = Product.objects.get(pk=product_id)
#         try:
#             exist_order = CartItem.objects.get(product=product, cart=self)
#             product.stock += exist_order.quantity
#             product.save()
#             exist_order.delete()
#         except CartItem.DoesNotExist:
#             pass


# # def pre_save_cart_reciver(sender, instance, action, *args, **kwargs):
# #     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
# #         items = instance.product.all()

# #         total = 0
# #         for item in items:
# #             total += item.price
# #         instance.total = total
# #         instance.save()


# # m2m_changed.connect(pre_save_cart_reciver, sender=Cart.product.through)


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()

#     def clear_cart(self, request):
#         try:
#             cart = Cart.objects.get(user=request.user)
#             items = CartItem.objects.filter(cart=cart)

#             items.delete()
#         except CartItem.DoesNotExist:
#             pass

#     def __str__(self):
#         return f'{self.product.title} برای کارت شماره : {self.cart.id}'

# class Cart(object):

#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)

#         if not cart:  # ye cart e khali ba un session barash besaz
#             cart = self.session[settings.CART_SESSION_ID] = {}

#         self.cart = cart

#     # product o be cart ezafe mikone ya quantity sho update mikone
#     def add(self, product, quantity, update_quantity=False):
#         product_id = str(product.id)
#         cart = self.cart
#         if product_id not in cart:
#             cart[product_id] = {'quantity': 0, 'price': str(product.price)}

#         if update_quantity:
#             cart[product_id]['quantity'] = quantity

#         else:
#             cart[product_id]['quantity'] += quantity

#         self.save()

#     def remove(self, product):
#         product_id = str(product.id)
#         cart = self.cart
#         if product_id in cart:
#             del cart[product_id]

#             self.save()

#     def save(self):
#         # session e cart o update mikone
#         self.session[settings.CART_SESSION_ID] = self.cart
#         # session o mark mikone ta motmaen she hamechi save shude
#         self.session.modified = True

#     def __iter__(self):
#         # iterate mikone item haye dakhele cart ro baad product haro az database migire
#         product_ids = self.cart.keys()
#         products = Product.objects.filter(id__in=product_ids)

#         for product in products:
#             self.cart[str(product.id)]['product'] = product

#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item

#     def count(self):
#         # counter e item haye dakhele cart e
#         return sum(item['quantity'] for item in self.cart.values())
