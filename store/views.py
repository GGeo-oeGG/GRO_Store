from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)

from store.mixins import (
    OwnerOnlyMixin,
    FilterByNameMixin,
    create_tags_mixin,
    update_tags_mixin,
    info_tags_mixin,
    list_tags_mixin,
    delete_tags_mixin
)
from store.models import (
    Product,
    SubCategory,
    Category
)
from store.serializers import (
    ProductSerializer,
    SubCategorySerializer,
    CategorySerializer
)


@list_tags_mixin
class BaseListView(ListAPIView):
    """ Вывод списков с фильтрацией по имени. """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


@info_tags_mixin
class BaseDetailView(RetrieveAPIView):
    """ Просмотр деталей объекта. """

    pass


# region Product

@create_tags_mixin
class CreateProduct(CreateAPIView):
    """Создание продукта."""

    serializer_class = ProductSerializer


@update_tags_mixin
class UpdateProduct(OwnerOnlyMixin, UpdateAPIView):
    """Редактирование продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class InfoProduct(BaseDetailView):
    """Подробная информация продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProduct(FilterByNameMixin, BaseListView):
    """Список продуктов."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


@delete_tags_mixin
class DeleteProduct(OwnerOnlyMixin, DestroyAPIView):
    """Удаление продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# endregion
# region Category

@create_tags_mixin
class CreateCategory(CreateAPIView):
    """Создание категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@update_tags_mixin
class UpdateCategory(OwnerOnlyMixin, UpdateAPIView):
    """Редактирование категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class InfoCategory(BaseDetailView):
    """Подробная информация категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListCategory(FilterByNameMixin, BaseListView):
    """Список категорий."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@delete_tags_mixin
class DeleteCategory(OwnerOnlyMixin, DestroyAPIView):
    """Удаление категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# endregion
# region SubCategory

@create_tags_mixin
class CreateSubCategory(CreateAPIView):
    """Создание под_категории."""

    serializer_class = SubCategorySerializer


@update_tags_mixin
class UpdateSubCategory(OwnerOnlyMixin, UpdateAPIView):
    """Редактирование под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class InfoSubCategory(BaseDetailView):
    """Подробная информация под_категории."""

    serializer_class = SubCategorySerializer


class ListSubCategory(FilterByNameMixin, BaseListView):
    """Список под_категорий."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


@delete_tags_mixin
class DeleteSubCategory(OwnerOnlyMixin, DestroyAPIView):
    """Удаление под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()

# endregion
