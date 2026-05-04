from django.urls import path

from users.views import CreateCustomUser, CustomUserDetail, DeleteCustomUser, UpdateCustomUser

app_name = 'users'

urlpatterns = [
    path('user/create/', CreateCustomUser.as_view(), name='user_create'),
    path('user/detail/<int:pk>/', CustomUserDetail.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', UpdateCustomUser.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', DeleteCustomUser.as_view(), name='user_delete'),

]
