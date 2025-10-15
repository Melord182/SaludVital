"""
Serializadores para la API REST del sistema de gestión de clínica.
Transforman los modelos Django en formato JSON y viceversa.
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