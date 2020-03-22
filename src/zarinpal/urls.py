from django.urls import path
from .views import send_request, verify, send_request2, verify2

urlpatterns = [

    path('request/', send_request, name='request'),
    path('request2/', send_request2, name='request2'),

    path('verify/', verify, name='verify'),
    path('verify2/', verify2, name='verify2'),
]
