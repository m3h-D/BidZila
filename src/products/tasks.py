
import time
from datetime import datetime, timedelta
from django.utils import timezone
from celery.schedules import crontab
# from background_task import background
from celery import task, shared_task
from haraji.celery import app
from products.models import Product
from userspends.models import UserWinner
from spendations.models import Spend
from django.shortcuts import get_object_or_404
from celery.task import periodic_task

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# def remove_afk(userspend_f, product):

#     # if product.event_end <= p:

#     userspend_f.delete()
#     product.session_key = ' '
#     product.save()
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# schedule.every(1).minutes.do(remove_afk)

# @periodic_task(run_every=crontab(minute="*/30"))
@task
def remove_afk():
    # product = Product.objects.filter(ended=False)
    # uspendf = UserSpend.objects.filter(
    #     user_can=True, user_ended=False).order_by('-timestamp').first()

    # if uspendf.created <= timezone.now():
    #     uspendf.delete()
    products = Product.objects.all()
    for product in products:
        product.save()
    # spends = Spend.objects.all()
    # for spend in spends:
    #     spend.save()
    userwinners = UserWinner.objects.all()
    for user in userwinners:
        user.save()

    # if product.ended == False:
    # p = timezone.now()
    # if prod.event_end <= p:

    # uspendf.user_can = False
    # uspendf.spending = 0
    # uspendf.new_price = 0
    # uspendf.save()


@task
def winner_email(userspend):
    product = get_object_or_404(Product, pk=userspend)
    userspend_w = Spend.objects.filter(user_can=True,
                                       product=product).order_by('-new_price', '-timestamp').first()

    subject, from_email, to = 'برنده شدی', 'lordofhell225@gmail.com', userspend_w.user.email
    # send_mail(subject, comment, from_email, to, fail_silently=True)
    # messages.success(request, '')

    html_content = render_to_string(
        'products/winner.html', {'userspend_w': userspend_w})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


app.conf.beat_schedule = {
    'remove_afk': {
        'task': 'products.tasks.remove_afk',
        'schedule': 5.0,

    },
}
app.conf.timezone = 'UTC'
