"""
Archivo: admin.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este archivo configura el **panel de administración de Django (Django Admin)** para el sistema de gestión de clínica.
El objetivo es registrar todos los modelos de la aplicación y definir cómo se visualizarán y gestionarán sus datos 
desde la interfaz administrativa.  

Django Admin es una herramienta integrada en el framework que permite a los administradores manejar el contenido 
del sistema de forma gráfica, sin necesidad de escribir código.

FUNCIONALIDAD PRINCIPAL:
------------------------
Cada modelo (como Paciente, Medico, Especialidad, etc.) se registra con una clase personalizada que hereda 
de `admin.ModelAdmin`. Estas clases permiten controlar:

- **list_display** → Campos visibles en la tabla principal del admin.  
- **list_filter** → Filtros laterales para facilitar la búsqueda.  
- **search_fields** → Campos sobre los que se puede buscar mediante texto.  
- **ordering** → Ordenamiento predeterminado de los registros.  
- **date_hierarchy** → Barra de navegación por fechas (si aplica).

VENTAJAS DE ESTA CONFIGURACIÓN:
-------------------------------
✔ Mejora la legibilidad y accesibilidad de los datos.  
✔ Permite a los administradores gestionar la información clínica de forma eficiente.  
✔ Centraliza la administración de pacientes, médicos, tratamientos y recetas.  
✔ Aprovecha las relaciones entre modelos (como médico-especialidad o paciente-consulta).  

DEPENDENCIAS:
-------------
- `django.contrib.admin`: Módulo base para la administración.  
- `.models`: Importa todos los modelos definidos en la aplicación.  

CONCLUSIÓN:
-----------
Este archivo convierte los modelos de la base de datos en entidades administrables dentro del panel de Django,
proporcionando una interfaz completa para la gestión clínica sin necesidad de desarrollo adicional.
"""

from django.contrib import admin
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica
)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Especialidad.
    """
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Paciente.
    """
    list_display = ['rut', 'nombre_completo', 'fecha_nacimiento', 'prevision', 'activo']
    list_filter = ['prevision', 'activo']
    search_fields = ['rut', 'nombre', 'apellido_paterno', 'apellido_materno']
    ordering = ['apellido_paterno', 'apellido_materno', 'nombre']


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Medico.
    """
    list_display = ['rut', 'nombre_completo', 'especialidad', 'jornada', 'activo']
    list_filter = ['especialidad', 'jornada', 'activo']
    search_fields = ['rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'numero_registro']
    ordering = ['apellido_paterno', 'apellido_materno', 'nombre']


@admin.register(ConsultaMedica)
class ConsultaMedicaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ConsultaMedica.
    """
    list_display = ['id', 'paciente', 'medico', 'fecha_hora', 'estado']
    list_filter = ['estado', 'medico__especialidad', 'fecha_hora']
    search_fields = ['paciente__nombre', 'medico__nombre', 'diagnostico']
    ordering = ['-fecha_hora']
    date_hierarchy = 'fecha_hora'


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Medicamento.
    """
    list_display = ['nombre', 'principio_activo', 'laboratorio', 'stock_disponible', 'requiere_receta', 'activo']
    list_filter = ['requiere_receta', 'activo', 'laboratorio']
    search_fields = ['nombre', 'principio_activo', 'laboratorio']
    ordering = ['nombre']


@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Tratamiento.
    """
    list_display = ['id', 'consulta', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo', 'fecha_inicio']
    search_fields = ['descripcion', 'consulta__paciente__nombre']
    ordering = ['-fecha_inicio']
    date_hierarchy = 'fecha_inicio'


@admin.register(RecetaMedica)
class RecetaMedicaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para RecetaMedica.
    """
    list_display = ['id', 'tratamiento', 'medicamento', 'dosis', 'frecuencia', 'fecha_emision']
    list_filter = ['fecha_emision', 'medicamento']
    search_fields = ['medicamento__nombre', 'tratamiento__consulta__paciente__nombre']
    ordering = ['-fecha_emision']
    date_hierarchy = 'fecha_emision'