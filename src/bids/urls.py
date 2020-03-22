from .views import bids_view, bid_detail
from django.urls import path


urlpatterns = [
    path('list/', bids_view, name="bids_view"),
    path('<id>/<slug>/', bid_detail, name="bid_detail"),
]
