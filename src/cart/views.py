from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .cart import Cart
from .bidcart import BidCart
from .forms import CartAddProductForm, CartAddBidForm
# from .models import Cart, CartItem
from products.models import Product
from userspends.models import UserSpend
from spendations.models import Spend
from bids.models import Bid

from accounts.forms import UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile


# def add_to_cart(request, product_id):
#     if request.user.is_authenticated:
#         try:
#             product = Product.objects.get(pk=product_id)
#         except ObjectDoesNotExist:  # id i ke vojod nadashte bashe vase ye product
#             pass

#         else:
#             try:
#                 cart = Cart.objects.get(user=request.user, active=True)
#             except ObjectDoesNotExist:
#                 cart = Cart.objects.create(user=request.user)
#                 cart.save()
#             if product.stock == 0:
#                 product.save()
#                 messages.success(
#                     request, f"محصول  '{product.title}'  به تعدادکافی موجود نیست")
#                 return redirect('cart:cart')
#             else:
#                 product.stock -= 1
#                 product.save()
#             cart.add_to_cart(product_id)

#         return redirect('cart:cart')

#     else:
#         return redirect('login-view')


# def remove_from_cart(request, product_id):
#     if request.user.is_authenticated:
#         try:
#             product = Product.objects.get(pk=product_id)
#         except ObjectDoesNotExist:
#             pass

#         else:
#             cart = Cart.objects.get(user=request.user, active=True)
#             cart.remove_from_cart(product_id)
#             product.stock += 1
#             product.save()

#         return redirect('cart:cart')
#     else:
#         return redirect('pages:home-page')


# def clear_from_cart(request, product_id):
#     if request.user.is_authenticated:
#         try:
#             product = Product.objects.get(pk=product_id)
#         except ObjectDoesNotExist:
#             pass

#         else:
#             cart = Cart.objects.get(user=request.user.id, active=True)
#             cart.clear_from_cart(product_id)

#         return redirect('cart:cart')
#     else:
#         return redirect('pages:home-page')


# def clear_cart(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.get(user=request.user, active=True)
#         items = CartItem.objects.filter(cart=cart)
#         for item in items:
#             item.clear_cart(request)

#         return redirect('cart:cart')
#     else:
#         return redirect('pages:home-page')


# def get_total_price(request):
#     cart = Cart.objects.get(user=request.user.id, active=True)
#     return cart.total


# @login_required
# def cart(request):
#     message = messages.get_messages(request)
#     # cart, new_obj = Cart.objects.new_or_get(request)
#     # items = cart.product.all()
#     # ---------------[asli]--------------------------------
#     try:
#         cart = Cart.objects.get(user=request.user.id, active=True)
#         items = CartItem.objects.filter(cart=cart)
#     except ObjectDoesNotExist:
#         cart = Cart.objects.create(user=request.user)
#         items = CartItem.objects.filter(cart=cart)
#     # -----------------------------------------------------

#     total = 0
#     count = 0
#     for item in items:
#         total += (item.product.price * item.quantity)
#         count += item.quantity
#     cart.total = total
#     cart.save()

#     context = {
#         'cart': items,
#         'total': total,
#         'count': count,
#         'messages': message,

#     }

#     return render(request, 'cart/detail.html', context)


# @login_required
# def bank_view(request):
#     try:
#         cart = Cart.objects.get(user=request.user.id, active=True)
#         items = CartItem.objects.filter(cart=cart)
#     except ObjectDoesNotExist:
#         cart = Cart.objects.create(user=request.user)
#         items = CartItem.objects.filter(cart=cart)
#     total = cart.total

#     if request.method == "POST":
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(
#             request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             return redirect('zarinpal:request')

#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#         'cart': items,
#         'total': total
#     }
#     return render(request, 'cart/bank.html', context)


# def add_to_cart_product_list(request, product_id):
#     if request.user.is_authenticated:
#         try:
#             product = Product.objects.get(pk=product_id)
#         except ObjectDoesNotExist:  # id i ke vojod nadashte bashe vase ye product
#             pass

#         else:
#             try:
#                 cart = Cart.objects.get(user=request.user, active=True)
#             except ObjectDoesNotExist:
#                 cart = Cart.objects.create(user=request.user)
#                 cart.save()
#             if product.stock == 0:
#                 product.save()
#                 messages.success(
#                     request, f"محصول  '{product.title}'  به تعدادکافی موجود نیست")
#                 return redirect('cart:cart')
#             else:
#                 product.stock -= 1
#                 product.save()
#             cart.add_to_cart(product_id)
#             messages.success(
#                 request, f"محصول  '{product.title}' به سبد خرید اضافه شد")
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#     else:
#         return redirect('login-view')

# ---------- bid_cart ---------------


@require_POST
def add_to_bid_cart(request, id):

    bid_cart = BidCart(request)
    bid = get_object_or_404(Bid, id=id)
    form = CartAddBidForm(request.POST)
    if bid.stack == 0:
        messages.success(
            request, f"محصول  '{bid.title}'  به تعدادکافی موجود نیست")
        return redirect('cart:bid_cart_view')
    else:
        messages.success(
            request, f"محصول  '{bid.title}' به سبد خرید اضافه شد")
        if form.is_valid():
            cd = form.cleaned_data
            bid_cart.add(bid=bid,
                         quantity=cd['quantity'], update_quantity=cd['update'])

        return redirect('cart:bid_cart_view')


def remove_from_bid_cart(request, id):
    bid_cart = BidCart(request)
    bid = get_object_or_404(Bid, id=id)
    bid.stack += 1
    bid.save()
    bid_cart.remove(bid)
    return redirect('cart:bid_cart_view')


# ------------------ cart--------------------
@require_POST
def add_to_cart(request, id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    # p_session = Product.objects.filter(id=product.id).first()
    # u_session = Spend.objects.filter(
    #     product=product, user_can=True).order_by('-new_price', '-timestamp').first()
    # qty = request.session.get('quantity', None)
    # print(qty)
    spend = Spend.objects.get(product=product, user=request.user)
    # if product.user_session == u_session.user_session:
    form = CartAddProductForm(request.POST)

    if product.stack == 0:
        messages.success(
            request, f"محصول  '{product.title}'  به تعدادکافی موجود نیست")
        return redirect('cart:cart')
    else:
        messages.success(
            request, f"محصول  '{product.title}' به سبد خرید اضافه شد")
        if form.is_valid():
            spend.user_ended = True
            spend.save()
            cd = form.cleaned_data
            cart.add(product=product,
                     user=request.user,
                     quantity=cd['quantity'], update_quantity=cd['update'])

        return redirect('cart:cart')
    # else:
    #     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    spend = Spend.objects.get(product=product, user=request.user)
    product.stack += 1
    product.save()
    cart.remove(product)
    spend.user_ended = False
    spend.save()
    return redirect('cart:cart')


def cart(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})  # *****
        spend = Spend.objects.filter(
            user=request.user, product=item['product'])
        if spend:
            return render(request, 'cart/detail.html', {'cart': cart, 'spend': spend})
    # for x in cart:
    #     print(x['product'])
    #     spend = Spend.objects.filter(user=request.user, product=x['product'])
    #     if spend:

    #         return render(request, 'cart/detail.html', {'cart': cart, 'spend': spend})
    return render(request, 'cart/detail.html', {'cart': cart})


def bid_cart_view(request):
    bid_cart = BidCart(request)
    for item in bid_cart:
        item['update_quantity_form'] = CartAddBidForm(
            initial={'quantity': item['quantity'], 'update': True})  # *****

    return render(request, 'cart/detail2.html', {'bid_cart': bid_cart})
