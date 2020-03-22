from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver

from .utils import uuid_generator
from .models import Order
from accounts.models import Profile


@receiver(pre_save, sender=Order)
def pre_save_code_generator(sender, instance, *args, **kwargs):
    if not instance.uuidcode:
        instance.uuidcode = uuid_generator(instance)


# @receiver(post_save, sender=Order)
# def post_save_profile(sender, instance, *args, **kwargs):
#     try:
#         profile = Profile.objects.get(user=instance, order=instance)
#     except Profile.DoesNotExist:
#         profile = Profile.objects.create(user=instance, order=instance)
#         profile.save()
