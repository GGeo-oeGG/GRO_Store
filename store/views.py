from django.db.models import F, FloatField, Prefetch, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.mixins import cart_tags_mixin, category_tags_mixin, product_tags_mixin, sub_category_tags_mixin
from store.models import Cart, CartProduct, Category, Product, ProductImages, SubCategory
from store.serializers import CartProductSerializer, CategorySerializer, ProductSerializer, SubCategorySerializer


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
    page_size = 100
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=ProductImages.objects.order_by('order'))
    )


@product_tags_mixin
class DeleteProduct(DestroyAPIView):
    """Удаление продукта."""

    serializer_class = ProductSerializer


# endregion
# region Category

@category_tags_mixin
class CreateCategory(CreateAPIView):
    """Создание категории."""

    serializer_class = CategorySerializer


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
        'category',
        Prefetch('product', queryset=Product.objects.prefetch_related('images'))
    )


@category_tags_mixin
class ListCategory(BaseListView):
    """Список категорий."""

    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        'category',
        Prefetch('product', queryset=Product.objects.prefetch_related('images'))
    )


@category_tags_mixin
class DeleteCategory(DestroyAPIView):
    """Удаление категории."""

    serializer_class = CategorySerializer


# endregion
# region SubCategory

@sub_category_tags_mixin
class CreateSubCategory(CreateAPIView):
    """Создание под_категории."""

    serializer_class = SubCategorySerializer


@sub_category_tags_mixin
class UpdateSubCategory(UpdateAPIView):
    """Редактирование под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


@sub_category_tags_mixin
class InfoSubCategory(BaseDetailView):
    """Подробная информация под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('product')


@sub_category_tags_mixin
class ListSubCategory(BaseListView):
    """Список под_категорий."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.prefetch_related('product')


@sub_category_tags_mixin
class DeleteSubCategory(DestroyAPIView):
    """Удаление под_категории."""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


# endregion
# region Cart

@cart_tags_mixin
class AddToCart(APIView):
    """Добавить продукт в корзину."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден'}, status=404)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()

        serializer = CartProductSerializer(cart_item)
        return Response(serializer.data, status=201)


@cart_tags_mixin
class UpdateCart(APIView):
    """Изменить количество продуктов в корзине."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request, item_id):
        quantity = request.data.get('quantity')
        if not quantity:
            return Response({'error': 'Укажите количество'}, status=400)

        try:
            cart_item = CartProduct.objects.get(id=item_id, cart__user=request.user)
        except CartProduct.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине'}, status=404)

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartProductSerializer(cart_item)
        return Response(serializer.data)


@cart_tags_mixin
class RemoveFromCart(APIView):
    """Удалить товар из корзины."""

    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, item_id):
        try:
            cart_item = CartProduct.objects.get(id=item_id, cart__user=request.user)
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
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
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
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=204)

# endregion
