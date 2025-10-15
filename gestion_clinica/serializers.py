"""
Archivo: serializers.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este archivo define los **serializadores (serializers)** utilizados por el sistema de gestión clínica 
para convertir los objetos del modelo Django en **formatos intercambiables (JSON)** y viceversa.  
Son un componente esencial de **Django REST Framework (DRF)**, permitiendo que los datos se envíen y reciban
a través de la API de forma estructurada y segura.

OBJETIVO:
---------
✔ Traducir los datos de los modelos a JSON para ser consumidos por el frontend o aplicaciones externas.  
✔ Validar la información entrante antes de crear o actualizar registros en la base de datos.  
✔ Incluir campos adicionales calculados o anidados (por ejemplo, edad, nombre completo, relaciones).  
✔ Mejorar la legibilidad y la eficiencia del consumo de datos clínicos.

INTEGRACIÓN CON LA API REST:
----------------------------
Cada serializador se asocia a un modelo y se usa dentro de las **vistas (ViewSets o APIViews)** del sistema.  
El flujo general de la API REST es:

1️⃣ Un cliente (frontend o aplicación móvil) realiza una solicitud HTTP (GET, POST, PUT, DELETE).  
2️⃣ La vista utiliza el serializador correspondiente para **validar** o **formatear** los datos.  
3️⃣ El serializador traduce el modelo Django en JSON (para respuesta) o valida el JSON recibido (para entrada).  
4️⃣ Django REST Framework gestiona automáticamente las respuestas serializadas y los códigos de estado HTTP.

TIPOS DE SERIALIZADORES USADOS:
-------------------------------
- `ModelSerializer`: crea un serializador basado automáticamente en un modelo Django.  
- `SerializerMethodField`: define campos calculados dinámicamente (por ejemplo, edad, cantidad_medicos).  
- `ReadOnlyField`: muestra datos calculados o derivados sin permitir su modificación.  
- `Nested Serializer`: permite incluir información relacionada (por ejemplo, especialidad dentro de médico).

DEPENDENCIAS:
-------------
- `rest_framework.serializers`: Librería principal de Django REST Framework.  
- `.models`: Modelos de datos definidos en el sistema clínico.

CONCLUSIÓN:
-----------
Los serializadores actúan como el **puente entre la base de datos y el exterior**, garantizando que la API REST 
entregue datos coherentes, validados y fácilmente interpretables por cualquier cliente.
"""

from rest_framework import serializers
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica
)


class EspecialidadSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Especialidad.
    """
    cantidad_medicos = serializers.SerializerMethodField()
    
    class Meta:
        model = Especialidad
        fields = '__all__'
    
    def get_cantidad_medicos(self, obj):
        return obj.medicos.filter(activo=True).count()


class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Paciente.
    """
    nombre_completo = serializers.ReadOnlyField()
    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = '__all__'
    
    def get_edad(self, obj):
        from datetime import date
        hoy = date.today()
        return hoy.year - obj.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day)
        )


class MedicoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Medico.
    """
    nombre_completo = serializers.ReadOnlyField()
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    
    class Meta:
        model = Medico
        fields = '__all__'


class MedicoDetalleSerializer(serializers.ModelSerializer):
    """
    Serializador detallado para el modelo Medico con información de la especialidad.
    """
    especialidad = EspecialidadSerializer(read_only=True)
    nombre_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Medico
        fields = '__all__'


class ConsultaMedicaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ConsultaMedica.
    """
    paciente_nombre = serializers.CharField(source='paciente.nombre_completo', read_only=True)
    medico_nombre = serializers.CharField(source='medico.nombre_completo', read_only=True)
    especialidad = serializers.CharField(source='medico.especialidad.nombre', read_only=True)
    
    class Meta:
        model = ConsultaMedica
        fields = '__all__'


class MedicamentoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Medicamento.
    """
    class Meta:
        model = Medicamento
        fields = '__all__'


class TratamientoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Tratamiento.
    """
    consulta_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Tratamiento
        fields = '__all__'
    
    def get_consulta_info(self, obj):
        return {
            'id': obj.consulta.id,
            'paciente': obj.consulta.paciente.nombre_completo,
            'medico': obj.consulta.medico.nombre_completo,
            'fecha': obj.consulta.fecha_hora
        }


class RecetaMedicaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo RecetaMedica.
    """
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True)
    tratamiento_info = serializers.SerializerMethodField()
    
    class Meta:
        model = RecetaMedica
        fields = '__all__'
    
    def get_tratamiento_info(self, obj):
        return {
            'id': obj.tratamiento.id,
            'descripcion': obj.tratamiento.descripcion,
            'paciente': obj.tratamiento.consulta.paciente.nombre_completo
        }