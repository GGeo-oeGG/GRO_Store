from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from unidecode import unidecode

from store.models import Cart
from users.permissions import OwnerOnlyPerm


class OwnerOnlyMixin:
    """ Доступ только владельцу."""

    permission_classes = [OwnerOnlyPerm, IsAuthenticated]


class GetOrCreateCartMixin:
    """ Получаем текущую корзину или создает новую. """

    def get_cart(self):
        user = self.request.user
        # Используем related_name "carts" из модели Cart
        cart, created = Cart.objects.get_or_create(owner=user)
        return cart


class FilterByNameMixin:  # TODO
    """ Фильтрация по имени. """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class ImageSerializeMixin:
    """ Обработка поля image для моделей. """

    image = serializers.ImageField(
        use_url=True,
        allow_empty_file=False,
        max_length=None
    )


class AutoSlugMixin:
    """ Добавление slug. """

    slug_field_name = 'slug'
    slug_from_field = 'name'

    def _generate_unique_slug(self):
        """ Добавляем уникальный slug. """

        base_text = unidecode(getattr(self, self.slug_from_field))
        base_slug = slugify(base_text)
        unique_slug = base_slug
        num = 1

        while self.__class__.objects.filter(**{self.slug_field_name: unique_slug}).exists():
            unique_slug = f'{base_slug}-{num}'
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):

        if not getattr(self, self.slug_field_name):
            setattr(self, self.slug_field_name, self._generate_unique_slug())
        super().save(*args, **kwargs)


def drf_spectacular_tags(tags_list):
    """ Декоратор для добавления тегов. """

    def decorator(cls):
        return extend_schema(tags=tags_list)(cls)

    return decorator


create_tags_mixin = drf_spectacular_tags(["Создать"])
update_tags_mixin = drf_spectacular_tags(["Обновить"])
info_tags_mixin = drf_spectacular_tags(["Информация"])
list_tags_mixin = drf_spectacular_tags(["Список"])
delete_tags_mixin = drf_spectacular_tags(["Удалить"])
