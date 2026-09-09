from config.settings import AUTH_USER_MODEL
from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from store.mixins import AutoSlugMixin


class Category(AutoSlugMixin, models.Model):
    """Категория продукта."""

    name = models.CharField(unique=True, max_length=50, verbose_name="категория")
    image = models.ImageField(
        upload_to="category/",
        null=True, blank=True,
        verbose_name="изображение"
    )
    slug = models.SlugField(unique=True, blank=True)  # blank = True - чтобы на пустое поле не ругалась админка

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "category"


class SubCategory(AutoSlugMixin, models.Model):
    """Подкатегория продукта."""

    name = models.CharField(unique=True, max_length=50, verbose_name="подкатегория")
    image = models.ImageField(
        upload_to="sub_category/",
        null=True, blank=True,
        verbose_name="изображение")
    category = models.ForeignKey(
        "Category",
        on_delete=SET_NULL,
        null=True,
        verbose_name="категория",
        related_name="sub_categories"
    )
    slug = models.SlugField(unique=True, blank=True)  # blank = True - чтобы на пустое поле не ругалась админка

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.name}"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        db_table = "sub_category"


class Product(AutoSlugMixin, models.Model):
    """Продукт."""

    name = models.CharField(unique=True, max_length=50, verbose_name="название")
    category = models.ForeignKey(
        "SubCategory",
        on_delete=SET_NULL,
        null=True,
        verbose_name="категория",
        related_name="products"
    )
    image = models.ImageField(
        upload_to="products/",
        null=True, blank=True,
        verbose_name="изображение",
        default="products/default_product.png"
    )
    slug = models.SlugField(unique=True, blank=True)  # blank = True - чтобы на пустое поле не ругалась админка
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="цена")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.name}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        db_table = "product"


class ProductImages(models.Model):
    """Изображения для продуктов."""

    product = models.ForeignKey("Product", on_delete=CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="products/",
        verbose_name="изображения",
        default="products/default_product.png"
    )
    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFill(100, 100)],
                                 format='JPEG',
                                 options={'quality': 85})
    image_medium = ImageSpecField(source='image',
                                  processors=[ResizeToFill(600, 600)],
                                  format='JPEG',
                                  options={'quality': 85})
    image_large = ImageSpecField(source='image',
                                 processors=[ResizeToFill(1200, 1200)],
                                 format='JPEG',
                                 options={'quality': 85})

    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.product}"

    class Meta:
        db_table = "product_images"


class Cart(models.Model):
    """Корзина."""

    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=PROTECT, related_name="carts")

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.owner}"

    class Meta:
        db_table = "cart"


class CartProduct(models.Model):
    """Промежуточная модель корзина-товар."""

    cart = models.ForeignKey("Cart", on_delete=SET_NULL, null=True, related_name="items")
    product = models.ForeignKey("Product", on_delete=SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        """Вывод удобного текста."""

        return f"{self.cart}"

    class Meta:
        unique_together = ("cart", "product")
        db_table = "cart_product"
