from rest_framework import serializers
from .models import *

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta: model = Especialidad; fields = "__all__"

# Repite el patrón para las demás entidades…
class SeguroSaludSerializer(serializers.ModelSerializer):
    class Meta: model = SeguroSalud; fields = "__all__"
class PacienteSerializer(serializers.ModelSerializer):
    class Meta: model = Paciente; fields = "__all__"
class MedicoSerializer(serializers.ModelSerializer):    
    class Meta: model = Medico; fields = "__all__"
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta: model = Medicamento; fields = "__all__"
class TratamientoSerializer(serializers.ModelSerializer):
    class Meta: model = Tratamiento; fields = "__all__"
class ConsultaMedicaSerializer(serializers.ModelSerializer):
    class Meta: model = ConsultaMedica; fields = "__all__"
class RecetaMedicaSerializer(serializers.ModelSerializer):
    class Meta: model = RecetaMedica; fields = "__all__"
