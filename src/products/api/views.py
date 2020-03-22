from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
# from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# from rest_framework.pagination import(
#     LimitOffsetPagination,
#     PageNumberPagination
# )

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django.db.models import Q

from products.models import Product

from .serializers import (
    ProductSerializers,
    ProductDetailSerializers,
    ProductCreateSerializers,
)

from .pagination import ProductLimitOffsetPagination, ProductPageNumberPagination


class ProductListAPIView(ListAPIView):
    """ 2 noe search darim yeki built-in e rest-framework e 
    yeki khudemoon ye func e get_queryset nvshtim"""
    # queryset = Product.objects.filter(
    #     available=True).order_by('-event', 'ended')
    serializer_class = ProductSerializers
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'slug']
    pagination_class = ProductPageNumberPagination
    # pagination_class = ProductLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        result = Product.objects.filter(
            available=True).order_by('-event', 'ended')
        # result = super(ProductListAPIView, self).get_queryset(*args, **kwargs)

        query = self.request.GET.get('q')
        if query:
            result = Product.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(slug__icontains=query)
            ).distinct()
        return result


class ProductUpdateAPIView(RetrieveUpdateAPIView):

    queryset = Product.objects.filter(available=True)
    serializer_class = ProductDetailSerializers


class ProductDeleteAPIView(DestroyAPIView):

    queryset = Product.objects.filter(available=True)
    serializer_class = ProductDetailSerializers


class RetrieveProductView(RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductDetailSerializers
    # lookup_field = 'slug'


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductCreateSerializers
    permission_classes = [IsAdminUser]

    # def perform_create(self, serializer):
    #     serializer.save(slug=self.title)
