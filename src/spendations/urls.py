from django.urls import path
from .views import add_to_spend, remove_from_spend,  delete_from_spend


urlpatterns = [
    path('add/<id>', add_to_spend, name='add_to_spend'),
    path('remove/<id>', remove_from_spend, name='remove_from_spend'),
    path('delete/<id>', delete_from_spend, name='delete_from_spend'),
]
