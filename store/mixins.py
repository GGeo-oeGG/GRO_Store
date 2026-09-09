from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from unidecode import unidecode


class ImageSerializeMixin:
    """Обработка поля image для моделей."""

    image = serializers.ImageField(
        use_url=True,
        allow_empty_file=False,
        allow_null=True,
        required=False,
        max_length=None
    )


class AutoSlugMixin:
    """Добавление slug."""

    slug_field_name = 'slug'
    slug_from_field = 'name'

    def _generate_unique_slug(self):
        """Добавляем уникальный slug."""
        base_text = unidecode(getattr(self, self.slug_from_field))
        base_slug = slugify(base_text)
        unique_slug = base_slug
        num = 1

        while self.__class__.objects.filter(**{self.slug_field_name: unique_slug}).exists():
            unique_slug = f'{base_slug}-{num}'
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        slug_value = getattr(self, self.slug_field_name)
        source_value = getattr(self, self.slug_from_field)
        if not slug_value and source_value:
            setattr(self, self.slug_field_name, self._generate_unique_slug())
        super().save(*args, **kwargs)


def drf_spectacular_tags(tags_list):
    """Добавление тегов для API-документации."""

    def decorator(cls):
        return extend_schema(tags=tags_list)(cls)

    return decorator


product_tags_mixin = drf_spectacular_tags(["Продукт"])
sub_category_tags_mixin = drf_spectacular_tags(["Под_категория"])
category_tags_mixin = drf_spectacular_tags(["Категория"])

cart_tags_mixin = drf_spectacular_tags(["Управление корзиной"])
