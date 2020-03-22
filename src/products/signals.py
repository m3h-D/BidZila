from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_save
from .models import Product
from django.utils import timezone
from datetime import timedelta
from userspends.models import UserSession, UserSpend, UserWinner
from spendations.models import Spend
from .tasks import winner_email
from bids.models import Bid
from orders.utils import product_uuid_generator
from cart.cart import Cart
from accounts.models import BidBoughts


# @receiver(post_save, sender=Product)
# def secret_key_signal_post(sender, instance, created, *args, **kwargs):
#     if created:
#         for x in instance.bid_buy.all():
#             x.secret_key = instance.secret_key
#             x.save()

# user_session_signal = Signal(providing_args=['instance', 'request'])


# @receiver(pre_save, sender=Product)
# def userspend_winner(sender, instance, *args, **kwargs):
#     userspend_f = UserSpend.objects.filter(
#         product__id=instance.id).order_by('-new_price').first()

#     if instance.event_end < timezone.now():
#         try:
#             if userspend_f:  # event ke end shud avalin user o user_can e sho true kon ta...
#                 userspend_f.user_can = True
#                 userspend_f.created = instance.event_end + \
#                     timedelta(minutes=1)
#                 userspend_f.save()
#                 # try:
#                 #     user_session = UserSession.objects.filter(
#                 #         user=userspend_f.user).order_by('-timestamp').first()  # akharin session_key e un user ke user_can e sh True ro migire
#                 #     userspend_f.user_session = user_session.user_session
#                 #     userspend_f.save()
#                 # except:
#                 #     user_session = UserSession.objects.filter(
#                 #         user=userspend_f.user).order_by('-timestamp').first()
#                 #     # print(user_session)
#                 #     userspend_f.user_session = user_session.user_session
#                 #     userspend_f.save()
#                 # if userspend_f.created <= timezone.now():
#                 #     # -------------------------------------------
#                 #     if userspend_f.user_can == True and userspend_f.user_ended == False:
#                 #         instance.event_end += timedelta(minutes=1)
#                 #         instance.save()
#                 #         userspend_f.delete()

#                 # instance.user_session = userspend_f.user_session
#                 # instance.final_price = userspend_f.new_price
#                 # instance.ended = True
#                 # instance.save()

#         except UserSpend.DoesNotExist:
#             userspend_f.user_can = False
#             userspend_f.save()

@receiver(pre_save, sender=Product)  # event key shuro she va key tamum she
def event_set(sender, instance, *args, **kwargs):
    if instance.event_start > timezone.now():
        instance.event = False
        instance.ended = False
        instance.reset = False
    if instance.event_start <= timezone.now() <= instance.event_end:
        instance.event = True
        instance.ended = False
        instance.reset = False
    if instance.event_end < timezone.now():
        instance.event = False
        instance.ended = True
        instance.out_of_user = False
        instance.secret_key = ''


# age barande baad az 2 saat kalaro nakharid mablaghe pishanadish ro 0 kon ta bere akhare jadval va nafare ghablish o winner kon
@receiver(pre_save, sender=Product)
def user_ended_signal(sender, instance, *args, **kwargs):
    # cart = Cart(instance)
    userspend_f = Spend.objects.filter(user_can=True, user_ended=False,
                                       product=instance).order_by('-new_price').first()
    # userwinner = UserWinner.objects.filter(product=instance)
    if instance.ended == True:
        if userspend_f:
            if userspend_f.created <= timezone.now() and userspend_f.new_price > 0:
                # if userspend_f.created <= timezone.now():
                # if userspend_f.user_can == True and userspend_f.user_ended == Falses:
                instance.event_end += timedelta(minutes=1)
                instance.user_session = ' '
                # userspend_f.delete()
                userspend_f.new_price = 0
                userspend_f.user_can = False
                userspend_f.status = 'transferred'
                # cart.remove(instance)
                userspend_f.save()  # in khat baaes mishe baade event timestamp user taghir kone
                instance.final_price = 0


# @receiver(pre_save, sender=Spend)
# def spend_user_session_signal(sender, instance, *args, **kwargs):
#     user_session = UserSession.objects.filter(
#         user=instance.user).order_by('-timestamp').first()
#     if instance.user_can == True:
#         instance.user_session = user_session.user_session


# age karbar avval shud user_can = True , gheymate pishnahadi mire to product, user_session ham mire to Spend
@receiver(pre_save, sender=Product)
def user_winner_signal(sender, instance, *args, **kwargs):

    userspend_f = Spend.objects.filter(
        product=instance).order_by('-new_price', '-last_spend').first()

    if instance.event_end < timezone.now():
        try:

            # event ke end shud avalin user o user_can e sho true kon ta...
            if userspend_f:
                user_session = UserSession.objects.filter(
                    user=userspend_f.user).order_by('-timestamp').first()
                if userspend_f.new_price > 0:
                    userspend_f.user_can = True
                    userspend_f.status = 'winner'
                    userspend_f.true_price = userspend_f.new_price
                    userspend_f.user_session = user_session.user_session
                    instance.final_price = userspend_f.new_price
                    if userspend_f.user_ended == False and userspend_f.email_send == False:
                        winner_email.delay(userspend=instance.pk)
                        userspend_f.email_send = True
                        userspend_f.save()

                userspend_f.created = instance.event_end + timedelta(minutes=1)
                userspend_f.save()  # *** in khat dare timestamp o update mikone

        except Spend.DoesNotExist:
            # userspend_f.user_can = False
            # userspend_f.save()
            pass


@receiver(pre_save, sender=Product)  # session_key e barande mire to product
def product_session_signal(sender, instance, *args, **kwargs):
    userspend_f = Spend.objects.filter(
        product=instance).order_by('-spending').first()
    if userspend_f:
        if userspend_f.user_can == True:
            instance.user_session = userspend_f.user_session


# @receiver(pre_save, sender=Product)
# def instance_reset_signal(sender, instance, *args, **kwargs):
#     if instance.reset == True:
#         instance.user.clear()
#         instance.reset = False


# age bekhayim ye mahsoolo dobare vase haraji bezarim dokme reset o mizanim ta pishnahada va kasaei ke join shudan pak shan
@receiver(pre_save, sender=Product)
def product_reset_signal(sender, instance, *args, **kwargs):
    userspend = Spend.objects.filter(product=instance)
    # if instance.event == True and instance.reset == True:
    bidboughts = BidBoughts.objects.filter(product=instance)
    if instance.reset == True:

        instance.final_price = 0
        instance.user_session = ' '
        for bid in bidboughts:
            bid.delete()

        for x in userspend:
            x.delete()
        print(instance.user.all())
        instance.user.clear()

        # user.user_can == False
        # user.user_ended = False
        # user.save()
        # if instance.ended == False:
        # if instance.event == True or instance.ended == False:


# @receiver(pre_save, sender=Spend)
# def transmitions_user_won_signal(sender, instance, *args, **kwargs):
#     if instance.user_won == True:
#         UserWinner.objects.get_or_create(
#             user=instance.user, product=instance.product, spending=instance.spending, new_price=instance.new_price)


# ghrymate 30% ro hesab mikone mirize to precent_price
@receiver(pre_save, sender=Product)
def present_30_signal(sender, instance, *args, **kwargs):
    instance.precent_price = float(instance.true_price) * (30/100)


# age gheymate pishnahadi be 30% gheymate bazar resid kassi natune join she
@receiver(pre_save, sender=Product)
def out_of_user_signal(sender, instance, *args, **kwargs):
    userspend = Spend.objects.filter(
        product=instance).order_by('-spending').first()

    if userspend:
        if userspend.new_price >= instance.precent_price:
            instance.out_of_user = True
        elif userspend.new_price < instance.precent_price:
            instance.out_of_user = False
    else:
        instance.out_of_user = False


# meghdare takhfife hasel shude baraye winner
@receiver(pre_save, sender=UserWinner)
def userwinner_offered_signal(sender, instance, *args, **kwargs):
    instance.offered = ((float(instance.new_price) -
                         float(instance.product.true_price))/float(instance.product.true_price))*(-100)


# age nafare avval jaygahesh vagozar shud price 150% o bezar barash va vase kasaei ke baad az nafare avval hastan 150% takhfif bezar
@receiver(pre_save, sender=Product)
def price_looser_signal(sender, instance, *args, **kwargs):
    userspend = Spend.objects.filter(product=instance).order_by(
        '-new_price', '-last_spend').first()

    if instance.ended == True:
        if userspend:
            userspend_f = Spend.objects.filter(
                product=instance).order_by('-new_price', '-last_spend').exclude(user=userspend.user)
            bidbought = BidBoughts.objects.filter(
                user=userspend.user, product=instance)
            # for y in bidbought:
            total = sum(i.bid.price for i in bidbought)
            if userspend.user_can == False:
                userspend.true_price = instance.true_price - \
                    (total * (150/100))
                userspend.save()
            else:
                pass
            if userspend_f:

                for x in userspend_f:
                    if x.status != 'transferred':
                        x.status = 'looser'
                    bidboughts = BidBoughts.objects.filter(
                        user=x.user, product=instance)
                    total = sum(i.bid.price for i in bidboughts)

                    # for z in bidboughts:

                    x.true_price = instance.true_price - (total * (150/100))
                    x.save()

            else:
                pass


# secret_key vase mahsool misaze hamono be bid hash mide ta bid ha makhsus e khude mahsool bashe
@receiver(pre_save, sender=Product)
def secret_key_signal(sender, instance, *args, **kwargs):
    # bids = Bid.objects.filter(products__in=instance)
    if instance.ended == False:
        instance.secret_key = product_uuid_generator(instance)
    if instance.pk is not None:
        if instance.ended == False:

            for x in instance.bid_buy.all():
                x.secret_key = instance.secret_key
                x.save()
    # if bids in instance.bid_buy:
    # for bids in instance.bid_buy:
    # bids.secret_key = instance.secret_key
    # bids.save()


# 10sec e akhar age pishnahad biad 10 sec vaghte bishtar mishe
@receiver(pre_save, sender=Product)
def event_end_set_signal(sender, instance, *args, **kwargs):

    userspend = Spend.objects.filter(product=instance).order_by(
        '-new_price', '-last_spend').first()
    time = instance.event_end - timedelta(seconds=10)
    # print(time)
    if instance.event == True:
        if userspend:
            user_qty = 0
            if userspend.last_spend <= time:
                user_qty = userspend.quantity
            if time <= timezone.now() and userspend.quantity > user_qty:
                instance.event_end += timedelta(seconds=10)


# age nafare user_can mahsoolo kharid baghie 2 saat vaght daran mahsoolo bekharan
# @receiver(pre_save, sender=Product)
# def lossers_time_to_buy(sender, instance, *args, **kwargs):
#     userspend_f = Spend.objects.filter(product=instance, user_can=True).order_by(
#         '-new_price', '-timestamp').first()
#     if instance.ended == True:
#         if userspend_f:
#             # userspend = Spend.objects.filter(
#             #     product=instance).exclude(user=userspend_f.user)

#             # or (userspend_f.user_can == False and userspend_f.user_won == False):
#             if userspend_f.user_won == True:
#                 user_win = UserWinner.objects.get(
#                     product=instance, user=userspend_f.user)
#                 time = user_win.created + timedelta(hours=2)
#                 # email
#                 if time <= timezone.now():
#                     instance.cannot_buy = True
#                     # for user in userspend:
#                     #     user.true_price = 0
#                     #     user.save()
 # ------------------ ya in  ------------------------------------


# @receiver(pre_save, sender=Product)
# def lossers_time_to_buy(sender, instance, *args, **kwargs):
#     userspend_f = Spend.objects.filter(product=instance, user_can=True).order_by(
#         '-new_price', '-timestamp').first()
#     if instance.ended == True:
#         if userspend_f:
#             userspend = Spend.objects.filter(
#                 product=instance).exclude(user=userspend_f.user)

#             # or (userspend_f.user_can == False and userspend_f.user_won == False):
#             if userspend_f.user_won == True:

#                 user_win = UserWinner.objects.get(
#                     product=instance, user=userspend_f.user)
#                 time = user_win.created + timedelta(hours=2)
#                 for x in userspend:
#                     x.created = time

#                     if x.time <= timezone.now():
#                         instance.cannot_buy = True

                # # email
