"""
Filtros personalizados para la API REST del sistema de gestión de clínica.
Permite filtrar datos por campos específicos de cada modelo.
"""

import django_filters
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica
)


class EspecialidadFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de especialidades.
    """
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    activa = django_filters.BooleanFilter()
    
    class Meta:
        model = Especialidad
        fields = ['nombre', 'activa']


class PacienteFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de pacientes.
    """
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='apellido_paterno', lookup_expr='icontains')
    rut = django_filters.CharFilter(lookup_expr='icontains')
    prevision = django_filters.ChoiceFilter(choices=Paciente.PREVISION_CHOICES)
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'rut', 'prevision', 'activo']


class MedicoFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de médicos por especialidad y otros campos.
    """
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='apellido_paterno', lookup_expr='icontains')
    especialidad = django_filters.NumberFilter(field_name='especialidad__id')
    especialidad_nombre = django_filters.CharFilter(field_name='especialidad__nombre', lookup_expr='icontains')
    jornada = django_filters.ChoiceFilter(choices=Medico.JORNADA_CHOICES)
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Medico
        fields = ['nombre', 'apellido', 'especialidad', 'especialidad_nombre', 'jornada', 'activo']


class ConsultaMedicaFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de consultas médicas por médico, paciente y estado.
    """
    medico = django_filters.NumberFilter(field_name='medico__id')
    paciente = django_filters.NumberFilter(field_name='paciente__id')
    especialidad = django_filters.NumberFilter(field_name='medico__especialidad__id')
    estado = django_filters.ChoiceFilter(choices=ConsultaMedica.ESTADO_CHOICES)
    fecha_desde = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='lte')
    
    class Meta:
        model = ConsultaMedica
        fields = ['medico', 'paciente', 'especialidad', 'estado', 'fecha_desde', 'fecha_hasta']


class MedicamentoFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de medicamentos.
    """
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    principio_activo = django_filters.CharFilter(lookup_expr='icontains')
    laboratorio = django_filters.CharFilter(lookup_expr='icontains')
    requiere_receta = django_filters.BooleanFilter()
    activo = django_filters.BooleanFilter()
    
    class Meta:
        model = Medicamento
        fields = ['nombre', 'principio_activo', 'laboratorio', 'requiere_receta', 'activo']


class TratamientoFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de tratamientos.
    """
    consulta = django_filters.NumberFilter(field_name='consulta__id')
    paciente = django_filters.NumberFilter(field_name='consulta__paciente__id')
    medico = django_filters.NumberFilter(field_name='consulta__medico__id')
    activo = django_filters.BooleanFilter()
    fecha_inicio = django_filters.DateFilter()
    
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'paciente', 'medico', 'activo', 'fecha_inicio']


class RecetaMedicaFilter(django_filters.FilterSet):
    """
    Filtro para búsqueda de recetas médicas.
    """
    tratamiento = django_filters.NumberFilter(field_name='tratamiento__id')
    medicamento = django_filters.NumberFilter(field_name='medicamento__id')
    paciente = django_filters.NumberFilter(field_name='tratamiento__consulta__paciente__id')
    fecha_desde = django_filters.DateFilter(field_name='fecha_emision', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_emision', lookup_expr='lte')
    
    class Meta:
        model = RecetaMedica
        fields = ['tratamiento', 'medicamento', 'paciente', 'fecha_desde', 'fecha_hasta']