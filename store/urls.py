from django.urls import path

from store.views import (
    AddToCart,
    ClearCart,
    CreateCategory,
    CreateProduct,
    CreateSubCategory,
    DeleteCategory,
    DeleteProduct,
    DeleteSubCategory,
    InfoCart,
    InfoCategory,
    InfoProduct,
    InfoSubCategory,
    ListCategory,
    ListProduct,
    ListSubCategory,
    RemoveFromCart,
    UpdateCart,
    UpdateCategory,
    UpdateProduct,
    UpdateSubCategory,
)

app_name = 'store'

urlpatterns = [
    path('category/create/', CreateCategory.as_view(), name='category_create'),
    path('category/update/<int:pk>/', UpdateCategory.as_view(), name='category_update'),
    path('category/info/<int:pk>/', InfoCategory.as_view(), name='category_info'),
    path('category/list/', ListCategory.as_view(), name='category_list'),
    path('category/delete/<int:pk>/', DeleteCategory.as_view(), name='category_delete'),

    path('sub_category/create/', CreateSubCategory.as_view(), name='sub_category_create'),
    path('sub_category/update/<int:pk>/', UpdateSubCategory.as_view(), name='sub_category_update'),
    path('sub_category/info/<int:pk>/', InfoSubCategory.as_view(), name='sub_category_info'),
    path('sub_category/list/', ListSubCategory.as_view(), name='sub_category_list'),
    path('sub_category/delete/<int:pk>/', DeleteSubCategory.as_view(), name='sub_category_delete'),

    path('product/create/', CreateProduct.as_view(), name='product_create'),
    path('product/update/<int:pk>/', UpdateProduct.as_view(), name='product_update'),
    path('product/info/<int:pk>/', InfoProduct.as_view(), name='product_info'),
    path('product/list/', ListProduct.as_view(), name='product_list'),
    path('product/delete/<int:pk>/', DeleteProduct.as_view(), name='product_delete'),

    path('cart/add/', AddToCart.as_view(), name='cart_add-item'),
    path('cart/update/', UpdateCart.as_view(), name='cart_update'),
    path('cart/remove/', RemoveFromCart.as_view(), name='cart_remove_item'),
    path('cart/info/', InfoCart.as_view(), name='cart_info'),
    path('cart/clear/', ClearCart.as_view(), name='cart_clear'),
]
