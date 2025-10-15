from django import forms
from .models import (
    SeguroSalud,
    Especialidad,
    Paciente,
    Medico,
    Medicamento,
    Tratamiento,
    ConsultaMedica,
    RecetaMedica,
)

# ---------------------------------------------------
# FORMULARIOS BASE CRUD
# ---------------------------------------------------

class SeguroSaludForm(forms.ModelForm):
    class Meta:
        model = SeguroSalud
        fields = ["nombre", "contacto"]


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ["nombre", "descripcion"]


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "rut",
            "nombres",
            "apellidos",
            "genero",
            "fecha_nacimiento",
            "seguro",
        ]


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            "rut",
            "nombres",
            "apellidos",
            "especialidad",
        ]


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ["nombre", "descripcion"]


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ["nombre", "descripcion", "medicamentos"]


class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = [
            "paciente",
            "medico",
            "fecha",
            "motivo",
            "estado",
        ]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = [
            "consulta",
            "indicaciones",
            "medicamentos",
        ]
