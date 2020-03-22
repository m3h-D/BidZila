from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Spend
# from .spend import Spend

from products.models import Product
from .forms import SpendForm
from accounts.models import BidBoughts
from django.utils import timezone
# Create your views here.


# def add_to_spend(request, id):
#     spend = Spend(request)
#     product = get_object_or_404(Product, id=id)
#     form = SpendForm(request.POST or None)
#     if form.is_valid():
#         cd = form.cleaned_data
#         spend.add(product=product,
#                   quantity=cd['quantity'], update_quantity=cd['update'])

#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# def remove_from_spend(request, id):
#     spend = Spend(request)
#     product = get_object_or_404(Product, id=id)
#     spend.remove(product)
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def spend_cal(spend, product):
    spend.spending = spend.quantity * product.can_spend.spend
    spend.new_price = spend.spending + product.new_price
    spend.save()


def add_to_spend(request, id):
    product = get_object_or_404(Product, pk=id)
    new_spend = product.new_price + product.can_spend.spend
    try:
        spend = Spend.objects.get(user=request.user, product=product)

        bidboughts = BidBoughts.objects.filter(
            user=spend.user, product=product, ended=False).order_by('created').first()
        if bidboughts:
            if bidboughts.ended == False:
                if bidboughts.amount <= 0:
                    bidboughts.ended = True
                    bidboughts.amount = 0
                    bidboughts.save()
                if spend.new_price < product.true_price and bidboughts.amount > 0:
                    spend.quantity += 1
                    spend.last_spend = timezone.now()
                    bidboughts.amount -= product.can_spend.mult
                    bidboughts.save()

                spend_cal(spend, product)
            else:
                pass
        else:
            pass
    except Spend.DoesNotExist:
        if request.user.bidboughts.filter(product=product).count() > 0:
            spend = Spend.objects.create(user=request.user,
                                         product=product,
                                         new_price=new_spend,
                                         spending=product.can_spend.spend,
                                         quantity=1,
                                         last_spend=timezone.now()
                                         )
            spend.save()
            bidboughts = BidBoughts.objects.filter(
                user=spend.user, product=product, ended=False).order_by('created').first()
            if bidboughts:
                if bidboughts.ended == False:
                    if bidboughts.amount <= 0:
                        bidboughts.ended = True
                        bidboughts.amount = 0
                        bidboughts.save()
                    elif bidboughts.amount > 0:
                        bidboughts.amount -= product.can_spend.mult
                        bidboughts.save()
                spend.save()
            else:
                pass

    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return redirect(product.get_absolute_url())


def remove_from_spend(request, id):
    product = get_object_or_404(Product, pk=id)
    try:
        spend = Spend.objects.get(user=request.user, product=product)
        if spend.quantity < 2:
            spend.delete()
        else:
            spend.quantity -= 1
            spend_cal(spend, product)
    except Spend.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_from_spend(request, id):
    product = get_object_or_404(Product, pk=id)
    try:
        spend = Spend.objects.get(user=request.user, product=product)
        spend.delete()
    except Spend.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
