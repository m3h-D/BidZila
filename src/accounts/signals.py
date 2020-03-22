from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
# from django.dispatch import Signal


# user_logged_in = Signal(providing_args=['instance', 'request'])


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # field e user to table profile o por kon
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
