from django.urls import path
from .views import contact_view, home_view

urlpatterns = [
    path('contact/', contact_view, name='contact-view'),
    path('', home_view, name='home-view'),

]
