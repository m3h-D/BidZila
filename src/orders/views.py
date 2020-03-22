from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, OrderItem
from cart.cart import Cart
from cart.bidcart import BidCart
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from payments.models import Payment
from accounts.models import Profile, BidBoughts
from accounts.forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.


# def order_created(request):
#     cart = Cart(request)
#     if request.method == "POST":
#         order = Order.objects.create(
#             paid=False,
#             status='created',
#         )
#         cart = Cart(request)
#         for item in cart:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item['product'],
#                 price=item['price'],
#             )
#         cart.clear()
#         request.session['order_id'] = order.id

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
#         'cart': cart,
#     }
#     return render(request, 'orders/bank.html', context)
@staff_member_required
def orders(request):
    orders = Order.objects.all().order_by('-created')
    return render(request, 'orders/list.html', {'orders': orders})


def order_detail(request, id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=id)
        order_product = OrderItem.objects.filter(order=order)
        payment = Payment.objects.filter(order_id=order)
        amount_order = Order.get_total_cost(order)
        return render(request, 'orders/detail.html', {'order': order, 'order_product': order_product, 'payment': payment, 'amount_order': amount_order, })
    else:
        return redirect('accounts:login-view')


# @login_required
# def bank_view(request):

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
#     return render(request, 'orders/bank.html', context)

@login_required
def order_created(request):

    cart = Cart(request)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

        order = Order.objects.create(paid=False,
                                     status='created',
                                     user=request.user,
                                     )

        for item in cart:

            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])

            cart.clear()

        # set the order in the session
        request.session['order_id'] = order.id

        return redirect('zarinpal:request')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cart': cart,

    }
    return render(request, 'orders/bank.html', context)


@login_required
def bid_order_created(request):
    bid = BidCart(request)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

        order = Order.objects.create(paid=False,
                                     status='created',
                                     user=request.user,
                                     )
        bid = BidCart(request)
        for x in bid:

            OrderItem.objects.create(order=order,
                                     bids=x['bid'],
                                     price=x['price'],
                                     quantity=x['quantity'])

            bid.clear()

        # set the order in the session
        request.session['bid_order_id'] = order.id

        return redirect('zarinpal:request2')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'bid': bid,

    }
    return render(request, 'orders/bank2.html', context)


def wallet_order_create(request):
    if 'wallet_price' in request.session:
        price = request.session['wallet_price']
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()

            price = request.session['wallet_price']
            order = Order.objects.create(paid=False,
                                         status='created',
                                         types='gateway',
                                         user=request.user)
            OrderItem.objects.create(order=order,
                                     price=price,
                                     quantity=1)
            del request.session['wallet_price']
            request.session['order_wallet_id'] = order.id
            return redirect('zarinpal:request')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'price': price,
        }
        return render(request, 'orders/bank3.html', context)
    else:
        return redirect("accounts:wallet")


def bid_order_Wallet_created(request):
    bid = BidCart(request)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

        order = Order.objects.create(paid=False,
                                     status='created',
                                     types='wallet',
                                     user=request.user,
                                     )
        bid = BidCart(request)
        for x in bid:

            order_item = OrderItem.objects.create(order=order,
                                                  bids=x['bid'],
                                                  price=x['price'],
                                                  quantity=x['quantity'])

            bid.clear()

        # set the order in the session
        request.session['bid_wallet_order_id'] = order.id
        bid_wallet_order_id = request.session.get('bid_wallet_order_id', None)
        if bid_wallet_order_id:
            order_obj = Order.objects.get(
                id=bid_wallet_order_id, user=request.user)
            order_items = OrderItem.objects.filter(order=order)
            total_price = int(order_obj.get_total_cost())
            for item in order_items:
                bidamount = item.bids.amount * item.quantity

                bid_bought = BidBoughts.objects.create(user=order_obj.user,
                                                       bid=item.bids,
                                                       product=item.bids.products.filter(
                                                           secret_key=item.bids.secret_key).first(),
                                                       title=item.bids.title,
                                                       amount=bidamount,
                                                       secret_key=item.bids.secret_key)
                bid_bought.user.profile.wallet -= total_price
                bid_bought.user.profile.save()
                bid_bought.save()
            messages.success(
                request, f'{order_item.bids.title} برای این محصول اضافه شد ')
        else:
            messages.error(
                request, f' بید برای این محصول اضافه نشد ')
        return redirect(order_item.bids.products.filter(secret_key=order_item.bids.secret_key).first())
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'bid': bid,

    }
    return render(request, 'orders/bank4.html', context)
