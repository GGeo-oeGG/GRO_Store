from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CurrentCustomUserMixin:
    """Ограничение доступа только к текущему пользователю."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

def drf_spectacular_tags(tags_list):
    """Декоратор для добавления тегов в документации."""

    def decorator(cls):
        return extend_schema(tags=tags_list)(cls)
    return decorator

users_tags_mixin = drf_spectacular_tags(["CRUD для users"])
