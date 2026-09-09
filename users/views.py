from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.mixins import CurrentCustomUserMixin, users_tags_mixin
from users.permissions import OwnerOnlyPerm
from users.serializers import CustomUserSerializer


@users_tags_mixin
class CreateCustomUser(CurrentCustomUserMixin, CreateAPIView):
    """Создание пользователя."""

    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer


@users_tags_mixin
class UpdateCustomUser(CurrentCustomUserMixin, RetrieveUpdateAPIView):
    """Редактирование пользователя."""

    serializer_class = CustomUserSerializer


@users_tags_mixin
class CustomUserDetail(CurrentCustomUserMixin, RetrieveAPIView):
    """Просмотр данных пользователя."""

    serializer_class = CustomUserSerializer


@users_tags_mixin
class DeleteCustomUser(CurrentCustomUserMixin, DestroyAPIView):
    """Удаление пользователя."""

    permission_classes = [IsAuthenticated, OwnerOnlyPerm, ]
    serializer_class = CustomUserSerializer
