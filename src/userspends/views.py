from django.shortcuts import render, get_object_or_404
from .models import UserSpend
from products.models import Product
from spendations.spend import Spend
from django.http import HttpResponseRedirect
from django.db.models import Count, Max, Min

# Create your views here.


def user_spend_create(request):
    spend = Spend(request)

    # userspendi = UserSpend.objects.create(user=request.user)
    for item in spend:
        UserSpend.objects.update_or_create(user=request.user,
                                           new_price=item['new_price'],
                                           product=item['product'],
                                           spending=item['spending'],)

    unique_fields = ['product', 'user']

    duplicates = (
        UserSpend.objects.values(*unique_fields)
        .order_by()
        .annotate(max_id=Max('id'), count_id=Count('id'))
        .filter(count_id__gt=1)
    )

    for duplicate in duplicates:
        (
            UserSpend.objects
            .filter(**{x: duplicate[x] for x in unique_fields})
            .exclude(id=duplicate['max_id'])
            .delete()
        )

    # # First select the min ids
    # delete_same = UserSpend.objects.values(
    #     'new_price', 'spending').annotate(minid=Min('id')).order_by('new_price')
    # min_ids = [obj['minid'] for obj in delete_same]
    # # Now delete
    # UserSpend.objects.exclude(id__in=min_ids).delete()

    # request.session['userspend_id'] = userspend.id
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_userspend(request, id):
    product = get_object_or_404(Product, id=id)
    spend = Spend(request)

    userspend = UserSpend.objects.filter(
        user=request.user, product=product)
    userspend.delete()
    spend.remove(product)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
