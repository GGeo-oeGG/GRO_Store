from django.db.models import F, FloatField, Prefetch, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from store.mixins import (
    cart_tags_mixin,
    category_tags_mixin,
    product_tags_mixin,
    sub_category_tags_mixin)

from store.models import (
    Cart,
    CartProduct,
    Category,
    Product,
    ProductImages,
    SubCategory)
from store.serializers import (
    CartProductSerializer,
    CategorySerializer,
    ProductSerializer,
    SubCategorySerializer)


class StorePagination(PageNumberPagination):
    """ Настройки пагинации. """

    page_size = 100


class BaseListView(ListAPIView):
    """Вывод списков с фильтрацией по имени."""

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class BaseDetailView(RetrieveAPIView):
    """Просмотр деталей объекта."""

    pass


# region Product

@product_tags_mixin
class CreateProduct(CreateAPIView):
    """Создание продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


@product_tags_mixin
class UpdateProduct(UpdateAPIView):
    """Редактирование продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


@product_tags_mixin
class InfoProduct(BaseDetailView):
    """Подробная информация продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=ProductImages.objects.order_by('order'))
    )


@product_tags_mixin
class ListProduct(BaseListView):
    """Список продуктов."""

    serializer_class = ProductSerializer
    pagination_class = StorePagination
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=ProductImages.objects.order_by('order'))
    )


@product_tags_mixin
class DeleteProduct(DestroyAPIView):
    """Удаление продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# endregion
# region Category

@category_tags_mixin
class CreateCategory(CreateAPIView):
    """Создание категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@category_tags_mixin
class UpdateCategory(UpdateAPIView):
    """Редактирование категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@category_tags_mixin
class InfoCategory(BaseDetailView):
    """Подробная информация категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        Prefetch('sub_categories', queryset=SubCategory.objects.prefetch_related(
            Prefetch('products', queryset=Product.objects.prefetch_related('images'))
        ))
    )


@category_tags_mixin
class ListCategory(BaseListView):
    """Список категорий."""

    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        Prefetch('sub_categories', queryset=SubCategory.objects.prefetch_related(
            Prefetch('products', queryset=Product.objects.prefetch_related('images'))
        ))
    )


@category_tags_mixin
class DeleteCategory(DestroyAPIView):
    """Удаление категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# endregion
# region SubCategory

@sub_category_tags_mixin
class CreateSubCategory(CreateAPIView):
    """Создание под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


@sub_category_tags_mixin
class UpdateSubCategory(UpdateAPIView):
    """Редактирование под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


@sub_category_tags_mixin
class InfoSubCategory(BaseDetailView):
    """Подробная информация под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('products')


@sub_category_tags_mixin
class ListSubCategory(BaseListView):
    """Список под_категорий."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('products')


@sub_category_tags_mixin
class DeleteSubCategory(DestroyAPIView):
    """Удаление под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


# endregion
# region Cart

@cart_tags_mixin
class AddToCart(GenericAPIView):
    """Добавить продукт в корзину."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data.get('product')
        if product is None:
            return Response(
                {'error': 'Укажите товар'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        quantity = serializer.validated_data.get('quantity', 1)

        cart, _ = Cart.objects.get_or_create(owner=self.request.user)
        cart_item, created = CartProduct.objects.get_or_create(
            cart=cart, product=product
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            CartProductSerializer(cart_item).data, status=status.HTTP_201_CREATED
        )


@cart_tags_mixin
class UpdateCart(UpdateAPIView):
    """Изменить количество продуктов в корзине."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        return CartProduct.objects.filter(cart__owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@cart_tags_mixin
class RemoveFromCart(APIView):
    """Удалить товар из корзины."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        try:
            cart_item = CartProduct.objects.get(id=item_id, cart__owner=request.user)
            cart_item.delete()
            return Response({'message': 'Товар удалён из корзины'}, status=204)
        except CartProduct.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине'}, status=404)


@cart_tags_mixin
class InfoCart(APIView):
    """Информация о составе корзины."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(owner=request.user)
        cart.items.filter(product__isnull=True).delete()
        items = cart.items.select_related('product').all()
        serializer = CartProductSerializer(items, many=True)

        total_items = items.aggregate(total=Sum('quantity'))['total'] or 0

        total_price = items.aggregate(total=Sum(F('product__price') * F('quantity'), output_field=FloatField())
                                      )['total'] or 0.0

        return Response({
            'items': serializer.data,
            'total_items': total_items,
            'total_price': total_price,
        })


@cart_tags_mixin
class ClearCart(APIView):
    """Очистка корзины."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def delete(self, request):
        cart, created = Cart.objects.get_or_create(owner=request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=204)

# endregion
