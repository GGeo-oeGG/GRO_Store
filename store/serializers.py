from decimal import Decimal

from rest_framework import serializers

from store.mixins import ImageSerializeMixin
from store.models import (
    CartProduct,
    Category,
    Product,
    ProductImages,
    SubCategory,
)


class ProductImagesSerializer(serializers.ModelSerializer, ImageSerializeMixin):
    """Сериализатор изображений."""

    class Meta:
        model = ProductImages

        fields = ["image", "order"]
        read_only_fields = ["order"]


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product

        fields = ["name", "category", "slug", "images", "price"]
        read_only_fields = ["slug"]


class SubCategorySerializer(ImageSerializeMixin, serializers.ModelSerializer):
    """Сериализатор субкатегории."""

    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory

        fields = ["name", "slug", "image", "product"]
        read_only_fields = ["slug"]


class CategorySerializer(ImageSerializeMixin, serializers.ModelSerializer):
    """Сериализатор категории."""

    subcategory = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category

        fields = ["name", "slug", "image", "subcategory", ]
        read_only_fields = ["slug"]


class CartProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара в корзине."""

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

    def get_total_price(self, obj) -> Decimal:
        """Вычисляет стоимость позиции (цена * количество)."""

        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        """Проверка, что количество больше нуля."""

        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        return value
