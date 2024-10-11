from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
    )
from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, include

urlpatterns = [
    path('', include('django_prometheus.urls')),
    path('domain/', include('domain.urls')),
    path('health', include('health_check.urls')),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'),
    path('user/auth/token/', views.obtain_auth_token)
]
