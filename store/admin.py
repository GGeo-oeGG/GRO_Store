from django.contrib import admin

from store.models import Category, Product, SubCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение продукта в админ панели."""

    list_display = [
        "name",
        "price",
        "created_at",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категории в админ панели."""

    list_display = [
        "name",
        "image",
        "created_at",
    ]

    search_fields = ("name",)
    readonly_fields = ["created_at", "updated_at"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Отображение субкатегории в админ панели."""

    list_display = [
        "name",
        "image",
        "created_at",
    ]

    search_fields = ("name",)
    readonly_fields = ["created_at", "updated_at"]
