from django.contrib.auth import get_user_model, backends
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.conf import settings

UserModel = get_user_model()


class EmailBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(profile__phone__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return super().authenticate(request, username, password, **kwargs)
