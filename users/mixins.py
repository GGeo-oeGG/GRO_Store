from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from store.mixins import drf_spectacular_tags

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CurrentCustomUserMixin:
    """Ограничение доступа только к текущему пользователю."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


users_tags_mixin = drf_spectacular_tags(["CRUD для users"])
