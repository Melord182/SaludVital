from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import MedicoFilter, PacienteFilter, ConsultaFilter
# Create your views here.

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]; ordering_fields = ["nombre"]

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PacienteFilter
    search_fields = ["nombre","apellido","rut"]; ordering_fields = ["nombre","apellido","fecha_nacimiento"]

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedicoFilter
    search_fields = ["nombres","apellidos","rut","especialidad__nombre"]
    ordering_fields = ["nombres","apellidos"]

class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaMedicaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConsultaFilter
    search_fields = ["paciente__nombres","paciente__apellidos","paciente__rut","medico__nombres","medico__apellidos"]
    ordering_fields = ["fecha","estado"]

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]; ordering_fields = ["nombre"]

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]; ordering_fields = ["nombre"]

class RecetaMedicaViewSet(viewsets.ModelViewSet):
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["consulta__paciente__nombres","consulta__paciente__apellidos","consulta__paciente__rut","consulta__medico__nombres","consulta__medico__apellidos"]
    ordering_fields = ["consulta__fecha"]


# Repite el patrón para Paciente, Medico, ConsultaMedica, Tratamiento, Medicamento, RecetaMedica
