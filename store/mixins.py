from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from users.permissions import OwnerOnlyPerm


class OwnerOnlyMixin:
    """ Доступ только владельцу."""

    permission_classes = [OwnerOnlyPerm]


class FilterByNameMixin:
    """ Фильтрация по имени. """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


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