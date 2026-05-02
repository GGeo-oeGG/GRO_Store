from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from store.mixins import (
    create_tags_mixin,
    update_tags_mixin,
    info_tags_mixin,
    list_tags_mixin,
    delete_tags_mixin,
    GetOrCreateCartMixin,
    OwnerOnlyMixin
)
from store.models import (
    Product,
    SubCategory,
    Category,
    ProductImages,
    CartProduct,
    Cart
)
from store.serializers import (
    ProductSerializer,
    SubCategorySerializer,
    CategorySerializer,
    CartSerializer,
    CartProductSerializer
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
class UpdateProduct(UpdateAPIView):
    """Редактирование продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class InfoProduct(BaseDetailView):
    """Подробная информация продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=ProductImages.objects.order_by('order'))
    )


class ListProduct(BaseListView):
    """Список продуктов."""

    serializer_class = ProductSerializer
    page_size = 100
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=ProductImages.objects.order_by('order'))
    )


@delete_tags_mixin
class DeleteProduct(DestroyAPIView):
    """Удаление продукта."""

    serializer_class = ProductSerializer


# endregion
# region Category

@create_tags_mixin
class CreateCategory(CreateAPIView):
    """Создание категории."""

    serializer_class = CategorySerializer


@update_tags_mixin
class UpdateCategory(UpdateAPIView):
    """Редактирование категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class InfoCategory(BaseDetailView):
    """Подробная информация категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        'subcategory',
        Prefetch('product', queryset=Product.objects.prefetch_related('images'))
    )


class ListCategory(BaseListView):
    """Список категорий."""

    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        'subcategory',
        Prefetch('product', queryset=Product.objects.prefetch_related('images'))
    )


@delete_tags_mixin
class DeleteCategory(DestroyAPIView):
    """Удаление категории."""

    serializer_class = CategorySerializer


# endregion
# region SubCategory

@create_tags_mixin
class CreateSubCategory(CreateAPIView):
    """Создание под_категории."""

    serializer_class = SubCategorySerializer


@update_tags_mixin
class UpdateSubCategory(UpdateAPIView):
    """Редактирование под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class InfoSubCategory(BaseDetailView):
    """Подробная информация под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('product')


class ListSubCategory(BaseListView):
    """Список под_категорий."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('product')


@delete_tags_mixin
class DeleteSubCategory(DestroyAPIView):
    """Удаление под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


# endregion
# region Cart

class CartAPIView(APIView, OwnerOnlyMixin):
    """ Управление корзиной. """

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(owner=self.request.user)
        return cart

    def get(self, request):
        cart = self.get_cart()
        items = CartProduct.objects.filter(cart=cart)
        serializer = CartProductSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Добавить продукт в корзину или увеличить его количество. """

        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=HTTP_404_NOT_FOUND)

        cart = self.get_cart()
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartProductSerializer(cart_item)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def put(self, request, item_id):
        """ Изменить количество продукта в корзине. """

        quantity = request.data.get('quantity')
        try:
            cart_item = CartProduct.objects.get(id=item_id, cart__owner=self.request.user)
        except CartProduct.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartProductSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, item_id):
        """ Удалить продукт из корзины. """

        try:
            cart_item = CartProduct.objects.get(id=item_id, cart__owner=self.request.user)
            cart_item.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except CartProduct.DoesNotExist:
            return Response({'error': 'Элемент корзины не найден'}, status=HTTP_404_NOT_FOUND)

# endregion
