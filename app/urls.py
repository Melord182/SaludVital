from django.shortcuts import render
from .views import EspecialidadViewSet, PacienteViewSet, MedicoViewSet, MedicamentoViewSet, ConsultaMedicaViewSet, TratamientoViewSet, RecetaMedicaViewSet, TipoSangreViewSet, UserViewSet
from rest_framework import routers
from django.urls import path, include
#Aqui se configuran las rutas para cada vista, esto es lo que se llama cuando accedemos a la API
router = routers.DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'pacientes', PacienteViewSet)  
router.register(r'medicos', MedicoViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'consultas', ConsultaMedicaViewSet)
router.register(r'tratamientos', TratamientoViewSet)
router.register(r'recetas', RecetaMedicaViewSet)
router.register(r'tipos_sangre', TipoSangreViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]