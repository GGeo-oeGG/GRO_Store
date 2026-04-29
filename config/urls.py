from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

router = DefaultRouter()
urlpatterns = [
                  path('', RedirectView.as_view(url='api/docs/swagger/', permanent=False), name='hello_page'),
                  path('admin/', admin.site.urls),
                  path('users/', include('users.urls', namespace='users')),
                  path('store/', include('store.urls', namespace='store')),

                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

              ] + router.urls
