from django.shortcuts import render, get_object_or_404

from .models import Bid
# Create your views here.


def bids_view(request):
    bids = Bid.objects.filter(available=True)
    return render(request, 'bids/list.html', {"bids": bids})


def bid_detail(request, id, slug):
    bid = get_object_or_404(Bid, id=id, slug=slug)
    return render(request, 'bids/detail.html', {"bid": bid})
