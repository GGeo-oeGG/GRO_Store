from rest_framework import serializers

from store.mixins import ImageSerializeMixin
from store.models import (
    Category,
    SubCategory,
    Product,
    ProductImages,
    CartProduct,
    Cart
)


class ProductImagesSerializer(serializers.ModelSerializer, ImageSerializeMixin):
    """ Сериализатор изображений. """

    class Meta:
        model = ProductImages

        fields = ["image", "order"]
        read_only_fields = ["order"]


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор продукта. """

    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product

        fields = ["name", "category", "slug", "images", "price"]
        read_only_fields = ["slug"]


class SubCategorySerializer(ImageSerializeMixin, serializers.ModelSerializer):
    """ Сериализатор субкатегории. """

    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory

        fields = ["name", "slug", "image", "product"]
        read_only_fields = ["slug"]


class CategorySerializer(ImageSerializeMixin, serializers.ModelSerializer):
    """ Сериализатор категории. """

    subcategory = SubCategorySerializer(many=True, read_only=True)
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category

        fields = ["name", "slug", "image", "subcategory", "product"]
        read_only_fields = ["slug"]


class CartProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товара в корзине. """

    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=14, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'name', 'price', 'quantity', 'total_price']
        read_only_fields = ['id', 'name', 'price', 'total_price']
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def get_total_price(self, obj):
        """ Вычисляет стоимость позиции (цена * количество). """
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        """ Проверка, что количество больше нуля. """
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        return value


class CartSerializer(serializers.ModelSerializer):
    """ Сериализатор корзины. """

    items = CartProductSerializer(source='cartproduct_set', many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_quantity', 'total_sum']
        read_only_fields = ['owner']

    def get_total_quantity(self, obj):
        """ Суммирует количество всех товаров в корзине. """
        return sum(item.quantity for item in obj.cartproduct_set.all())

    def get_total_sum(self, obj):
        """ Суммирует стоимость всех товаров в корзине. """
        return sum(item.product.price * item.quantity for item in obj.cartproduct_set.all())
