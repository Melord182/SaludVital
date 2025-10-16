"""
Archivo: filters.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este archivo define los **filtros personalizados** que utiliza la API REST del sistema de gestión de clínica
para permitir a los usuarios realizar búsquedas y filtrados avanzados sobre los datos.

Los filtros están implementados mediante la librería **django-filter**, que se integra directamente con
Django REST Framework para procesar parámetros enviados en las URLs (por ejemplo: ?nombre=juan&activo=true).

Cada clase de filtro corresponde a un modelo del sistema (Paciente, Médico, Consulta, etc.) y permite
filtrar registros según campos específicos del modelo o de sus relaciones (por ejemplo: paciente__nombre o medico__especialidad).

OBJETIVO:
---------
✔ Mejorar la eficiencia de las consultas en la API.  
✔ Permitir búsquedas dinámicas sin necesidad de escribir código adicional.  
✔ Facilitar la integración con interfaces front-end (React, Vue, Angular, etc.).  
✔ Optimizar el rendimiento al trabajar con grandes volúmenes de datos médicos.

ESTRUCTURA DEL ARCHIVO:
-----------------------
- Cada clase hereda de `django_filters.FilterSet`.
- Dentro de cada clase se definen los filtros específicos por tipo de dato:
    • `CharFilter` → para texto (con `icontains` para búsquedas insensibles a mayúsculas).  
    • `BooleanFilter` → para valores booleanos.  
    • `ChoiceFilter` → para campos con opciones predefinidas.  
    • `DateFilter` → para filtrar por fechas (por ejemplo: fecha_desde / fecha_hasta).  
    • `NumberFilter` → para IDs o campos numéricos.  

FLUJO DE FUNCIONAMIENTO:
------------------------
1️⃣ El usuario realiza una petición a la API con parámetros en la URL (por ejemplo: `/api/pacientes/?nombre=ana`).  
2️⃣ Django REST Framework detecta el uso de `django-filter` y aplica los filtros definidos en este archivo.  
3️⃣ La vista devuelve solo los registros que cumplen las condiciones del filtro.  

DEPENDENCIAS:
-------------
- `django_filters`: Librería externa para filtrado de datos en DRF.
- `.models`: Se importan los modelos que serán filtrados.

CONCLUSIÓN:
-----------
Estos filtros hacen que la API sea flexible, eficiente y totalmente configurable, permitiendo búsquedas
específicas sobre pacientes, médicos, consultas, tratamientos y recetas médicas.
"""
import django_filters
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica, Laboratorio
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
# filters.py
class LaboratorioFilter(django_filters.FilterSet):
    pais = django_filters.ChoiceFilter(choices=[], label='País')
    activo = django_filters.ChoiceFilter(choices=[('', 'Todos'), ('true','Sí'), ('false','No')], method='filter_activo')

    class Meta:
        model = Laboratorio
        fields = ['pais', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # construir choices dinámicamente desde la BD (orden alfabético)
        paises = (self.queryset.values_list('pais', flat=True)
                               .distinct()
                               .order_by('pais'))
        self.filters['pais'].extra['choices'] = [('', 'Todos')] + [(p, p) for p in paises]

    def filter_activo(self, queryset, name, value):
        if value == 'true':  return queryset.filter(activo=True)
        if value == 'false': return queryset.filter(activo=False)
        return queryset

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
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    principio_activo = django_filters.CharFilter(lookup_expr='icontains')
    laboratorio = django_filters.NumberFilter(field_name='laboratorio__id')  # por id
    laboratorio_nombre = django_filters.CharFilter(field_name='laboratorio__nombre', lookup_expr='icontains')
    requiere_receta = django_filters.BooleanFilter()
    activo = django_filters.BooleanFilter()

    class Meta:
        model = Medicamento
        fields = ['nombre', 'principio_activo', 'laboratorio', 'laboratorio_nombre', 'requiere_receta', 'activo']

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