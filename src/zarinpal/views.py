from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from cart.cart import Cart
from payments.models import Payment
from zeep import Client

from orders.models import Order, OrderItem
from accounts.models import Profile, BidBoughts
# from products.models import Product
from userspends.models import UserSpend, UserWinner
from spendations.models import Spend

MERCHANT = '11111111-1111-1111-1111-111111111111'

client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')

# Toman / Required
#amount = 5000


description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

email = 'Lordofhell225@gmail.com'  # Optional

mobile = '09123456789'  # Optional

# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify/'


def get_order(request):
    order = request.session.get('order_id', None)
    return order


def get_bid_order(request):
    order = request.session.get('bid_order_id', None)
    return order


def get_wallet_order(request):
    order = request.session.get('order_wallet_id', None)
    return order


def send_request(request):
    order_wallet_id = get_wallet_order(request)
    if order_wallet_id:
        order_obj = Order.objects.get(id=order_wallet_id, user=request.user)
        order_obj.user = request.user
        order_obj.save()

        amount = int(order_obj.get_total_cost())

        # product = Product.objects.filter(id=order_obj.product.id)
        # product.ended = True
        # product.save()
        order_item = OrderItem.objects.filter(order=order_obj).first()
        if order_item.product == None and order_item.bids == None:
            profile_wallet = Profile.objects.get(user=order_obj.user)
            profile_wallet.wallet += order_item.price
            profile_wallet.save()

    order_id = get_order(request)
    if order_id:
        order_obj = Order.objects.get(id=order_id, user=request.user)
        order_obj.user = request.user
        order_obj.save()

        amount = int(order_obj.get_total_cost())

        # product = Product.objects.filter(id=order_obj.product.id)
        # product.ended = True
        # product.save()
        order_item = OrderItem.objects.filter(order=order_obj).first()
        # if order_item.product == None and order_item.bids == None:
        #     profile_wallet = Profile.objects.get(user=order_item.orders.user)
        #     profile_wallet.wallet += order_item.price
        #     profile_wallet.save()
        userspend = Spend.objects.filter(user_can=True,
                                         user__id=order_obj.user.id, product=order_item.product)
        userspend_l = Spend.objects.filter(user_can=False,
                                           user__id=order_obj.user.id, product=order_item.product)
        for x in userspend:
            x.user_ended = True
            x.user_won = True
            x.user_session = ''
            x.save()
            user_winner = UserWinner.objects.get_or_create(
                user=x.user, product=x.product, spending=x.spending, new_price=x.new_price)
        for y in userspend_l:
            y.user_ended = True
            y.save()

            # user_winner.save()
        profile_score = Profile.objects.get(user=order_obj.user)
        profile_score.score += 200
        profile_score.save()
    else:
        pass

    result = client.service.PaymentRequest(
        MERCHANT, amount, description, email, mobile, CallbackURL)

    if result.Status == 100:
        payment_obj = Payment.objects.create(
            user=order_obj.user,
            amount=amount,
            order_id=order_obj,
        )
        if order_wallet_id:
            del request.session['order_wallet_id']
        if order_id:
            del request.session['order_id']

        request.session['payment_id'] = payment_obj.id

        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))

    else:

        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):

    if request.GET.get('Status') == 'OK':
        payment_id = request.session.get('payment_id', None)

        if payment_id:
            payment_obj = Payment.objects.get(id=payment_id)

            amount = payment_obj.amount

            result = client.service.PaymentVerification(
                MERCHANT, request.GET['Authority'], amount)

        if result.Status == 100:
            cart = Cart(request)
            cart.clear()

            payment_obj.ref_id = result.RefID
            payment_obj.ref_status = result.Status
            payment_obj.save()

            try:
                del request.session['payment_id']
            except KeyError:
                pass

            order_obj = Order.objects.get(id=payment_obj.order_id.id)
            # order_item = OrderItem.objects.get(order=order_obj)
            order_obj.paid = True
            order_obj.status = 'paid'
            order_obj.save()

            product = Product.objects.filter(id=order_obj.product.id)
            product.ended = True
            product.save()

            # profile_score = Profile.objects.get(user=order_obj.user)
            # profile_score.score += 200
            # profile_score.save()

            context = {
                'refid': str(result.RefID),
                # 'custom':'',
                # 'orderpersonalinfo_obj': orderpersonalinfo_obj,

            }
            return render(request, 'payments/verify.html', context)

            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))

        elif result.Status == 101:

            return HttpResponse('Transaction submitted : ' + str(result.Status))

        else:

            payment_obj.status = result.Status
            payment_obj.save()

            order_obj = Order.objects.get(id=int(payment_obj.order_id.id))
            order_obj.status = 'canceled'
            order_obj.save()

            del request.session['payment_id']

            context = {
                'stat': str(result.Status),
                # 'profile': profile,

            }
            return render(request, 'payments/verify.html', context)

            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))

    else:

        payment_id = request.session.get('payment_id', None)
        if payment_id:

            payment_obj = get_object_or_404(Payment, id=payment_id)

            payment_obj.status = -111
            payment_obj.save()

            order_obj = Order.objects.get(id=int(payment_obj.oid.id))
            # orderpersonalinfo_obj=OrderPersonalInfo.objects.get(order=int(payment_obj.oid.id))

            order_obj.status = 'canceled'
            order_obj.save()

            del request.session['payment_id']

            context = {
                'err': -111,
                # 'orderpersonalinfo_obj': orderpersonalinfo_obj,

            }
            return render(request, 'payments/verify.html', context)

        return HttpResponse('Transaction failed or canceled by user')


def send_request2(request):

    order_id = get_bid_order(request)
    if order_id:
        order_obj = Order.objects.get(id=order_id, user=request.user)
        order_obj.user = request.user
        # order_item = OrderItem.objects.filter(order=order_obj)
        # for item in order_item:

        #     order_obj.user.profile.bids += item.bids.amount * item.quantity
        #     order_obj.user.profile.save()
        order_obj.save()
        order_item = OrderItem.objects.filter(order=order_obj)
        for item in order_item:
            bidamount = item.bids.amount * item.quantity
            # try:
            #     for x in item.bids.products.filter(secret_key=item.bids.secret_key):
            #         bid_bought = BidBoughts.objects.filter(
            #             product=x).first()
            #         if bid_bought:
            #             bid_bought.amount += bidamount
            #             bid_bought.save()

            # except BidBoughts.DoesNotExist:
            bid_bought = BidBoughts.objects.create(user=order_obj.user,
                                                   bid=item.bids,
                                                   product=item.bids.products.filter(
                                                       secret_key=item.bids.secret_key).first(),
                                                   title=item.bids.title,
                                                   amount=bidamount,
                                                   secret_key=item.bids.secret_key)
            bid_bought.user.profile.save()
            bid_bought.save()
            # order_obj.user.profile.have_bid = bid_bought

        amount = int(order_obj.get_total_cost())

        # --kife poooll---------------------------------

        # order_obj.user.profile.bid_have += order_obj.bid.amount
        # order_obj.save()

        # ---------------------------------------------

        # product = Product.objects.filter(id=order_obj.product.id)
        # product.ended = True
        # product.save()
        # order_item = OrderItem.objects.filter(order=order_obj).first()
        # userspend = Spend.objects.filter(
        #     user__id=order_obj.user.id, product=order_item.product)
        # for x in userspend:
        #     x.user_ended = True
        #     x.user_won = True
        #     x.user_session = ' '
        #     x.save()
    else:
        pass
    result = client.service.PaymentRequest(
        MERCHANT, amount, description, email, mobile, CallbackURL)

    if result.Status == 100:
        payment_obj = Payment.objects.create(
            user=order_obj.user,
            amount=amount,
            order_id=order_obj,
        )
        del request.session['bid_order_id']

        request.session['payment_id'] = payment_obj.id

        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))

    else:

        return HttpResponse('Error code: ' + str(result.Status))


def verify2(request):

    if request.GET.get('Status') == 'OK':
        payment_id = request.session.get('payment_id', None)

        if payment_id:
            payment_obj = Payment.objects.get(id=payment_id)

            amount = payment_obj.amount

            result = client.service.PaymentVerification(
                MERCHANT, request.GET['Authority'], amount)

        if result.Status == 100:
            cart = Cart(request)
            cart.clear()

            payment_obj.ref_id = result.RefID
            payment_obj.ref_status = result.Status
            payment_obj.save()

            try:
                del request.session['payment_id']
            except KeyError:
                pass

            order_obj = Order.objects.get(id=payment_obj.order_id.id)
            # order_item = OrderItem.objects.get(order=order_obj)
            order_obj.paid = True
            order_obj.status = 'paid'
            order_obj.save()

            product = Product.objects.filter(id=order_obj.product.id)
            product.ended = True
            product.save()

            profile_score = Profile.objects.get(user=order_obj.user)
            profile_score.score += 200
            profile_score.save()

            context = {
                'refid': str(result.RefID),
                # 'custom':'',
                # 'orderpersonalinfo_obj': orderpersonalinfo_obj,

            }
            return render(request, 'payments/verify.html', context)

            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))

        elif result.Status == 101:

            return HttpResponse('Transaction submitted : ' + str(result.Status))

        else:

            payment_obj.status = result.Status
            payment_obj.save()

            order_obj = Order.objects.get(id=int(payment_obj.order_id.id))
            order_obj.status = 'canceled'
            order_obj.save()

            del request.session['payment_id']

            context = {
                'stat': str(result.Status),
                # 'profile': profile,

            }
            return render(request, 'payments/verify.html', context)

            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))

    else:

        payment_id = request.session.get('payment_id', None)
        if payment_id:

            payment_obj = get_object_or_404(Payment, id=payment_id)

            payment_obj.status = -111
            payment_obj.save()

            order_obj = Order.objects.get(id=int(payment_obj.oid.id))
            # orderpersonalinfo_obj=OrderPersonalInfo.objects.get(order=int(payment_obj.oid.id))

            order_obj.status = 'canceled'
            order_obj.save()

            del request.session['payment_id']

            context = {
                'err': -111,
                # 'orderpersonalinfo_obj': orderpersonalinfo_obj,

            }
            return render(request, 'payments/verify.html', context)

        return HttpResponse('Transaction failed or canceled by user')
