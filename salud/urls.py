from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

# --- Importamos vistas API y HTML ---
from .views import EspecialidadViewSet
from .views_html import (
    HomeView,
    EspecialidadListView,
    EspecialidadCreateView,
    EspecialidadUpdateView,
    EspecialidadDeleteView,
)

# --- Namespace para la app ---
app_name = "salud"

# --- Router de Django REST Framework ---
router = DefaultRouter()
router.register(r"especialidades", EspecialidadViewSet, basename="especialidad")
router.register

# --- URLs HTML y API ---
urlpatterns = [
    # Página de inicio
    path("", HomeView.as_view(), name="home"),

    # CRUD de Especialidades (HTML)
    path("especialidades/", EspecialidadListView.as_view(), name="especialidad_list"),
    path("especialidades/nueva/", EspecialidadCreateView.as_view(), name="especialidad_create"),
    path("especialidades/<int:pk>/editar/", EspecialidadUpdateView.as_view(), name="especialidad_update"),
    path("especialidades/<int:pk>/eliminar/", EspecialidadDeleteView.as_view(), name="especialidad_delete"),

    # Endpoints REST API
    path("api/", include(router.urls)),
]
