# salud/filters.py
import django_filters
from .models import Medico, Paciente, ConsultaMedica

class MedicoFilter(django_filters.FilterSet):
    # permite /api/medicos/?especialidad=cardio
    especialidad = django_filters.CharFilter(
        field_name="especialidad__nombre", lookup_expr="icontains"
    )
    class Meta:
        model = Medico
        fields = ["especialidad"]

class PacienteFilter(django_filters.FilterSet):
    # permite /api/pacientes/?seguro=1&genero=M
    medico = django_filters.NumberFilter(field_name="consultamedica__medico__id")
    class Meta:
        model = Paciente
        fields = ["seguro", "genero"]

class ConsultaFilter(django_filters.FilterSet):
    # /api/consultas/?paciente_rut=123&medico_id=5&estado=AT
    paciente_rut = django_filters.CharFilter(field_name="paciente__rut")
    medico_id = django_filters.NumberFilter(field_name="medico__id")
    estado = django_filters.CharFilter(field_name="estado")
    class Meta:
        model = ConsultaMedica
        fields = ["paciente_rut", "medico_id", "estado"]
