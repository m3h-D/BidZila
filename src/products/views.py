from django.utils.timezone import now, localtime
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator


from cart.forms import CartAddProductForm
from accounts.models import Profile, BidBoughts
from spendations.forms import SpendForm
# from spendations.spend import Spend
from spendations.models import Spend
from spendations.views import remove_from_spend
from userspends.models import UserSpend, UserSession, UserWinner

from userspends.models import user_session_signal
from .models import Product, Category
from .tasks import remove_afk, winner_email
from django.core import serializers
import json


User = get_user_model()


# ---------------------  product-list -------------------


def product_list_view(request, cat_slug=None, category=None):
    message = messages.get_messages(request)
    categories = Category.objects.all().order_by(
        '-id')  # kolle category ha bedoone slug
    products = Product.objects.filter(
        available=True).order_by('-event', 'ended')
    try:
        for product in products:
            product.save()
    except:
        pass

    paginator = Paginator(products, 3)  # paginator baraye P_list_view
    page = request.GET.get('page')
    p = timezone.now()
    # baraye dast resi be product e har page... age ino nazarim to har page faqat 3 post e akha ro neshun mide
    products = paginator.get_page(page)

    if cat_slug:
        products = Product.objects.filter(
            available=True).order_by('-event', 'ended')
        # age ino dobare taarif nakonim products o paginator minine o dg produvt.obj bar nemigardoone
        category = get_object_or_404(Category, slug=cat_slug)
        # mire donbale product aei ke category e bala ro daran o peyda mikone
        products = products.filter(category=category)
        paginator = Paginator(products, 3)  # paginator baraye C_list_view
        page = request.GET.get('page')
        products = paginator.get_page(page)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        # 'products': json.dumps(products),
        'page': page,
        'message': message,
        'p': p,
    }
    return render(request, 'products/products_list.html', context)


# --------------product-detail-----------------------------------

def product_detail_view(request, pk, slug, is_user_p=False):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    userspend_w = Spend.objects.filter(user_can=True,
                                       product=product).order_by('-spending', '-timestamp').first()
    userspend = Spend.objects.filter(user_can=False,
                                     product=product).order_by('-new_price', '-timestamp')
    userspend_l = Spend.objects.filter(
        product=product).order_by('-new_price', '-timestamp')
    # spend = get_object_or_404(Spend, id=userspend_w)
    # spend = Spend(request)

    p = timezone.now()
    print('current time', p)
    # if product.event_start > p:
    #     product.event = False
    #     product.save()
    # if product.event_start <= p <= product.event_end:
    #     product.event = True
    #     product.save()
    # if product.event_end < p:
    # product.event = False
    # product.save()

    # userwinners = UserWinner.objects.all()
    # for user in userwinners:
    #     user.save()

    # try:
    # if userspend_f:  # event ke end shud avalin user o user_can e sho true kon ta...
    #     userspend_f.user_can = True
    #     userspend_f.created = product.event_end + timedelta(minutes=1)
    # if userspend is None:
    #     spend.remove(product=product)
    # try:
    #     # uspendf = serializers.serialize('json', [userspend_w, ])
    # produc = serializers.serialize('json', [product, ])

    #     if userspend_w and userspend_w.user_ended == False:
    #         winner_email.delay(userspend=pk)
    # except:
    #     pass

    # userspend_f.created += timedelta(minutes=1)
    # print('time userspend : ', userspend_f.created)

    # print(product.event_end, product.event, userspend_f.user_can)
    # ------------------------------------------------------------
    # try:
    #     user_session = UserSession.objects.filter(
    #         user=userspend_w.user).order_by('-timestamp').first()  # akharin session_key e un user ke user_can e sh True ro migire
    #     # print(user_session)
    #     # mirize to user_session e hamooni ke avval shude(user_can=True)
    #     userspend_w.user_session = user_session.user_session
    #     userspend_w.save()
    # except:
    # pass

    # userspend_f.save()
    # ---------- in event_ended ----------------
    # if userspend_f.created <= p:
    #     # -------------------------------------------
    #     if userspend_f.user_can == True and userspend_f.user_ended == False:
    #         # ---------- in clelery beat ---------------
    #         # remove_afk.delay()

    #         # ---------- in event_ended ----------------
    #         product.event_end += timedelta(minutes=1)
    #         product.save()
    #         userspend_f.delete()
    # ------------------------------------------
    # try:
    #     # session_key e uni ke aval shude ro mirize to session_key e product
    #     product.user_session = userspend_w.user_session
    #     # price i ke nafar e avval dade ro mirirze to product bara cart
    #     product.final_price = userspend_w.new_price
    #     product.save()
    # except:
    #     product.save()
    # if userspend_f.user_can == True and product.ended == False and product.event_end <= p:
    #     # uspendf = serializers.serialize('json', [userspend_f, ])
    #     # product = serializers.serialize('json', [product, ])
    #     remove_afk.delay(pk)

    # except UserSpend.DoesNotExist:
    #     userspend_f.user_can = False
    #     userspend_f.save()

    if product.user.filter(id=request.user.id).exists():  # vorod be haraji
        is_user_p = True

    message = messages.get_messages(request)

    # spend_form = SpendForm()
    cart_form = CartAddProductForm()
    # user_count = Spend.objects.filter(
    #     product=product, user_can=False, user_ended=False).count()
    user_count = product.user.all().count()

    # for x in product.user.all():
    users_in_spend = Spend.objects.filter(
        product=product)
    load_in = product.user.all().exclude(
        spend__in=users_in_spend)  # WOW what The Hell Was This?!!!

    # print(load_in)

    if request.user.is_authenticated:
        # ss = request.user.profile.have_bid.all()
        ss = BidBoughts.objects.filter(user=request.user, product=product)

        print(ss)
        all_u = Spend.objects.filter(
            product=product, user=request.user, product__ended=True)
        u = Spend.objects.filter(
            product=product, user=request.user).first()  # neshoon dadne winner e haraji dar soorati ke winner khudesh bud
        spend_s = Spend.objects.filter(
            product=product, user=request.user)
        spend_l = Spend.objects.filter(
            user=request.user, product__event=True)

        context = {
            'product': product,
            'u': u,
            'all_u': all_u,
            'ss': ss,
            'message': message,
            # 'spend_form': spend_form,
            # 'spend': spend,
            'userspend': userspend,
            'is_user_p': is_user_p,
            'spend_s': spend_s,
            'userspend_l': userspend_l,
            'cart_form': cart_form,
            'user_count': user_count,
            'p': p,
            'spend_l': spend_l,
            'load_in': load_in,
            'userspend_w': userspend_w,
        }

        return render(request, 'products/product_detail.html', context)
    else:
        # u = UserSpend.objects.filter(
        #     product=product).first()  # neshun dadane winner be user haei ke hatta login nakardan
        context = {
            'product': product,
            'message': message,
            # 'spend_form': spend_form,
            'userspend': userspend,
            'is_user_p': is_user_p,
            # 'spend': spend,
            # 'userspend_f': userspend_f,
            'userspend_l': userspend_l,
            'cart_form': cart_form,
            'user_count': user_count,
            'p': p,
            'userspend_w': userspend_w,

        }

    return render(request, 'products/product_detail.html', context)

# -------------------- Search ------------------------------------------


def search_view(request):
    categories = Category.objects.all().order_by(
        '-id')

    query = request.GET.get('q')
    result = Product.objects.filter(available=True).order_by('-event', 'ended')
    # user_filter = UserFilter(request.GET, queryset=result)
    if query:
        result = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(slug__icontains=query)
        ).distinct()

    paginator = Paginator(result, 6)
    page = request.GET.get('page')
    result = paginator.get_page(page)

    context = {
        'query': query,
        'result': result,
        'page': page,
        'item': result,
        'categories': categories,
    }

    return render(request, 'products/search.html', context)


# ------------ login into haraji -------------------------------------

def in_product(request, id, slug, is_user_p=False):
    if request.user.is_authenticated:
        # spend = Spend(request)
        product = get_object_or_404(Product, id=id, slug=slug)
        userspend = Spend.objects.filter(
            product=product, user=request.user)

        if product.user.filter(id=request.user.id).exists():
            product.user.remove(request.user)
            userspend.delete()
            # spend.remove(product=product)

            is_user_p = False
        else:
            product.user.add(request.user)
            is_user_p = True

        return redirect(product.get_absolute_url())
    else:
        product = get_object_or_404(Product, id=id, slug=slug)
        messages.success(
            request, f"برای ورود به مزایده ی محصول  ( {product.title} ) باید ثبت نام/وارد شوید")
        return redirect(product.get_absolute_url())


def product_detail_table(request, pk, slug, is_user_p=False):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    userspend_w = Spend.objects.filter(user_can=True,
                                       product=product).order_by('-spending', '-timestamp').first()
    userspend = Spend.objects.filter(user_can=False,
                                     product=product).order_by('-new_price', '-timestamp')
    userspend_l = Spend.objects.filter(
        product=product).order_by('-new_price', '-timestamp')
    if product.user.filter(id=request.user.id).exists():  # vorod be haraji
        is_user_p = True
    users_in_spend = Spend.objects.filter(
        product=product)
    load_in = product.user.all().exclude(
        spend__in=users_in_spend)
    context = {"product": product,
               "userspend": userspend,
               "userspend_l": userspend_l,
               "userspend_w": userspend_w,
               'load_in': load_in,
               'is_user_p': is_user_p,
               }
    return render(request, 'products/spend_table.html', context)
