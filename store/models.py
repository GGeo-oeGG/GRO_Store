from django.db import models
from django.db.models import SET_NULL, PROTECT, CASCADE
from django.utils.text import slugify
from config.settings import AUTH_USER_MODEL


class Category(models.Model):
    """ Категория продукта. """

    name = models.CharField(unique=True, verbose_name="категория")
    image = models.ImageField(upload_to="media/category/", null=True, blank=True, verbose_name="изображение")
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "category"


class SubCategory(models.Model):
    """ Подкатегория продукта. """

    name = models.CharField(unique=True, verbose_name="подкатегория")
    image = models.ImageField(upload_to="media/sub_category/", null=True, blank=True, verbose_name="изображение")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey("Category", on_delete=SET_NULL, null=True, verbose_name="категория",
                                 related_name="sub_categories")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        db_table = "sub_category"


class Product(models.Model):
    """ Продукт. """

    name = models.CharField(unique=True, verbose_name="название")
    image = models.ImageField(upload_to="media/products/", null=True, blank=True, verbose_name="изображение")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey("SubCategory", on_delete=SET_NULL, null=True, verbose_name="категория",
                                 related_name="products")
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="цена")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        db_table = "product"


class Cart(models.Model):
    """ Корзина. """

    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=PROTECT, related_name="carts")

    class Meta:
        db_table = "cart"


class CartProduct(models.Model):
    """ Промежуточная модель корзина-товар. """

    cart = models.ForeignKey("Cart", on_delete=CASCADE)
    product = models.ForeignKey("Product", on_delete=CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлён")

    class Meta:
        unique_together = ("cart", "product")
        db_table = "cart_product"
