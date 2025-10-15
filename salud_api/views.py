from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EspecialidadSerializer, PacienteSerializer, MedicoSerializer, MedicamentoSerializer, ConsultaMedicaSerializer, TratamientoSerializer, RecetaMedicaSerializer, TipoSangreSerializer, UserSerializer, LaboratorioSerializer
from .models import Especialidad, Paciente, Medico, Medicamento, Consulta_Medica, Tratamiento, Receta_Medica, Tipo_Sangre, User, Laboratorio
# Create your views here.

#Creamos las vistas para cada modelo, esto mostrara la api cuando la llamemos
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
class TipoSangreViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Sangre.objects.all()
    serializer_class = TipoSangreSerializer
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
class LaboratorioViewSet(viewsets.ModelViewSet):
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    queryset = Consulta_Medica.objects.all()
    serializer_class = ConsultaMedicaSerializer
class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
class RecetaMedicaViewSet(viewsets.ModelViewSet):
    queryset = Receta_Medica.objects.all()
    serializer_class = RecetaMedicaSerializer
#Cada vista hereda de viewsets.ModelViewSet que es una clase de Django Rest Framework que nos permite crear vistas basicas para nuestra API.
