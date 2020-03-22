from django.urls import path
from .views import (
    ProductListAPIView,
    RetrieveProductView,
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
)

urlpatterns = [
    path('product-list/', ProductListAPIView.as_view(), name='list_api'),
    path('product-list/create/',
         ProductCreateAPIView.as_view(), name='create_api'),
    path('product-retrieve/<pk>/',
         RetrieveProductView.as_view(), name='retrieve_api'),
    path('product-retrieve/<pk>/update/',
         ProductUpdateAPIView.as_view(), name='update_api'),
    path('product-retrieve/<pk>/delete/',
         ProductDeleteAPIView.as_view(), name='delete_api'),
    # path('product-retrieve/<slug>/',RetrieveProductView.as_view(), name='retrieve_api'),
]
