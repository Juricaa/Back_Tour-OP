from django.urls import path, include
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration de la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API TourOp",
        default_version='v1',
        description="Documentation interactive de l'API TourOp",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@tour-op.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [ 
    #    path('api/tutorials/', include('tutorials.urls')),
       path('api/clients/', include('clients.urls')),
       path('api/hebergements/', include('hebergements.urls')),
       path('api/voitures/', include('voitures.urls')),
       path('api/activites/', include('activites.urls')),
       path('api/vols/', include('vols.urls')),
       path('api/reservations/', include('reservations.urls')),
       path('api/factures/', include('factures.urls')),
       path('api/auth/', include('accounts.urls')),

       re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), # type: ignore
       path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # type: ignore
       path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # type: ignore
]
