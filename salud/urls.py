from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views import *
from .views_html import *
router = DefaultRouter()
router.register(r"especialidades", EspecialidadViewSet, basename="especialidad")
# Repite el patrón para las demás entidades…
router.register(r"pacientes", PacienteViewSet, basename="paciente")
router.register(r"medicos", MedicoViewSet, basename="medico")
router.register(r"consultas", ConsultaMedicaViewSet, basename="consultamedica")
router.register(r"tratamientos", TratamientoViewSet, basename="tratamiento")
router.register(r"medicamentos", MedicamentoViewSet, basename="medicamento")
router.register(r"recetas", RecetaMedicaViewSet, basename="recetamedica")
app_name = "salud"   # ← ← ← ¡IMPORTANTE!
# registrar los demás viewsets…
app_name = "salud"   # ← importante

urlpatterns = [ 
    path("", RedirectView.as_view(pattern_name="salud:especialidad_list", permanent=False)),
    path("api/", include(router.urls)),
    path("especialidades/", EspecialidadListView.as_view(), name="especialidad_list"),
    path("especialidades/nueva/", EspecialidadCreateView.as_view(), name="especialidad_create"),
    path("especialidades/<int:pk>/editar/", EspecialidadUpdateView.as_view(), name="especialidad_update"),
    path("especialidades/<int:pk>/eliminar/", EspecialidadDeleteView.as_view(), name="especialidad_delete"),
                ]
