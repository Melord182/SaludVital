#Importamos los modelos creados uno por uno e importamos serializers que es una clase de Django para poder crearlos.
from .models import Especialidad, Paciente, Medico, Medicamento, Consulta_Medica, Tratamiento, Receta_Medica, Tipo_Sangre, User
from rest_framework import serializers
#Aqui se crean los serializadores para convertir nuestros modelos (o tablas) en JSON para poder enviarlos mediante la API
class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
class TipoSangreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Sangre
        fields = '__all__'
class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'
class ConsultaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta_Medica
        fields = '__all__'
class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = '__all__'
class RecetaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta_Medica
        fields = '__all__'
