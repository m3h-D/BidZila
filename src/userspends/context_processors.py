from userspends.models import UserSpend, UserWinner
from spendations.models import Spend
from products.models import Product
from accounts.models import Profile
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def winners(request):
    latest = UserWinner.objects.all().order_by('-timestamp')[:10]
    return {'latest': latest}


def bids(request):
    if request.user.is_authenticated:
        bidss = Spend.objects.filter(
            user=request.user, product__event=True).order_by('-timestamp')
        return {'bids': bidss}
    else:
        bids = Spend.objects.filter(
            product__event=True, product__ended=True).order_by('-timestamp')
        return {'bids': bids}


def users(request):
    # if request.user.is_authenticated:

    users = Profile.objects.filter(score__gt=0).order_by('-score')

    return {'users': users}
