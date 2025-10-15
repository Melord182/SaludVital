from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# --- Swagger / documentación API ---
schema_view = get_schema_view(
    openapi.Info(
        title="API Clínica Vital",
        default_version="v1",
        description="Documentación de la API de Clínica Vital",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Incluimos las URLs de la app salud con namespace
    path("", include(("salud.urls", "salud"), namespace="salud")),

    # Documentación API
    re_path(r"^docs(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0),
         name="schema-redoc"),
]
