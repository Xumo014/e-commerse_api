
from django.contrib import admin
from django.urls import path, include, re_path
from billing.views import CreateChargeView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class JWTSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions['Bearer'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',

        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="My DRF API",
        default_version='v1',
        description="Bu API uchun Swagger hujjati",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="xtuxtamirzayev@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class = JWTSchemaGenerator

)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/v1/', include("products.urls")),

    path('api/v1/sms-auth/', include("users.urls")),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/pay/', CreateChargeView.as_view(), name='create_charge'),


    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

