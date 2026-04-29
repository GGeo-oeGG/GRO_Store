from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from users.views import (
    CreateCustomUser,
    UpdateCustomUser,
    CustomUserDetail,
    DeleteCustomUser)

app_name = 'users'

urlpatterns = [
    path('user/create/', CreateCustomUser.as_view(), name='user_create'),
    path('user/detail/<int:pk>/', CustomUserDetail.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', UpdateCustomUser.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', DeleteCustomUser.as_view(), name='user_delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]