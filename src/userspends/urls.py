from django.urls import path
from .views import user_spend_create, remove_from_userspend

urlpatterns = [
    path('create/', user_spend_create, name='user_spend_create'),
    path('remove/<id>/', remove_from_userspend, name='remove_from_userspend'),
]
