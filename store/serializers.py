from rest_framework import serializers

from store.models import (
    Category,
    SubCategory,
    Product
)


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор продукта. """

    class Meta:
        model = Product

        fields = ["name", "category", "slug", "image", "price", ]
        read_only_fields = ["slug"]


class SubCategorySerializer(serializers.ModelSerializer):
    """ Сериализатор субкатегории. """

    class Meta:
        model = SubCategory
        product = ProductSerializer(many=True, read_only=True)

        fields = ["name", "slug"]
        read_only_fields = ["slug"]


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор категории. """

    class Meta:
        model = Category

        subcategory = SubCategorySerializer(many=True, read_only=True)
        product = ProductSerializer(many=True, read_only=True)

        fields = ["name", "slug"]
        read_only_fields = ["slug"]
