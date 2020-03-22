# from django.dispatch import Signal, receiver
# from django.db.models.signals import pre_save, post_save

# from userspends.models import UserSession, UserSpend, UserWinner
# from spendations.models import Spend


# @receiver(pre_save, sender=Spend)
# def spend_user_session_signal(sender, instance, *args, **kwargs):
#     user_session = UserSession.objects.filter(
#         user=instance.user).order_by('-timestamp').first()
#     if instance.user_can == True:
#         instance.user_session = user_session.user_session


# @receiver(pre_save, sender=Spend)
# def transmitions_user_won_signal(sender, instance, *args, **kwargs):
#     if instance.user_won == True:
#         UserWinner.objects.get_or_create(
#             user=instance.user, product=instance.product, spending=instance.spending, new_price=instance.new_price)


# @receiver(pre_save, sender=UserWinner)
# def userwinner_offered_signal(sender, instance, *args, **kwargs):
