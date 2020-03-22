from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from products.models import Product


class ProductCreateSerializers(ModelSerializer):

    class Meta:
        model = Product
        exclude = (
            'id',
            'final_price',
            'available',
            'special',
            'precent_price',
            'out_of_user',
            'secret_key',
            'user',
            'user_session',
            'ended',
            'event',
            'cannot_buy',
            'image2',
            'image3',
        )


class ProductSerializers(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='products_api:retrieve_api')

    class Meta:
        model = Product
        exclude = ('description', 'image', 'image2', 'image3', 'true_price', 'final_price', 'stack',
                   'secret_key', 'user_session', 'created', 'updated', 'can_spend', 'bid_buy', 'user', 'slug', 'special', 'reset', 'precent_price')


class ProductDetailSerializers(ModelSerializer):
    delete_url = HyperlinkedIdentityField(view_name='products_api:delete_api')
    image = SerializerMethodField()

    class Meta:
        model = Product
        fields = ('__all__')

    def get_image(self, obj):
        return obj.image.url
