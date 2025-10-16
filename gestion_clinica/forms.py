from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica, Laboratorio
)


# -----------------------------
# Widgets comunes (HTML5)
# -----------------------------
DATE_INPUT_KW = {"type": "date"}
DATETIME_INPUT_KW = {"type": "datetime-local"}


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'activa']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'rut', 'nombre', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'telefono', 'email', 'direccion',
            'prevision', 'activo'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs=DATE_INPUT_KW),
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip()
        if len(rut) < 7:
            raise ValidationError("RUT inválido.")
        return rut


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['rut','nombre','apellido_paterno','apellido_materno',
                  'especialidad','telefono','email','numero_registro',
                  'jornada','fecha_ingreso','activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidad'].queryset = Especialidad.objects.filter(activa=True)
        # opcional: clases Bootstrap
        self.fields['especialidad'].widget.attrs.setdefault('class', 'form-select')

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'pais', 'direccion', 'telefono', 'email']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise ValidationError("El nombre del laboratorio es muy corto.")
        return nombre   

class ConsultaMedicaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica
        fields = [
            'paciente', 'medico', 'fecha_hora', 'motivo_consulta',
            'diagnostico', 'observaciones', 'estado'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs=DATETIME_INPUT_KW),
            'motivo_consulta': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)
        self.fields['medico'].queryset = Medico.objects.filter(activo=True)


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin', 'indicaciones', 'activo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs=DATE_INPUT_KW),
            'fecha_fin': forms.DateInput(attrs=DATE_INPUT_KW),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'indicaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Por tu lógica actual, solo consultas REALIZADAS para crear/editar tratamientos
        self.fields['consulta'].queryset = ConsultaMedica.objects.filter(estado='REALIZADA', paciente__activo=True)

    def clean(self):
        cleaned = super().clean()
        ini = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if ini and fin and fin < ini:
            self.add_error('fecha_fin', "La fecha de término no puede ser anterior al inicio.")
        return cleaned


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'nombre', 'principio_activo', 'presentacion', 'concentracion',
            'laboratorio', 'requiere_receta', 'stock_disponible', 'activo'
        ]

    def clean_stock_disponible(self):
        stock = self.cleaned_data['stock_disponible']
        if stock is None:
            return 0
        if stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return stock


class RecetaMedicaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica
        fields = [
            'tratamiento', 'medicamento', 'dosis', 'frecuencia',
            'duracion', 'cantidad_total', 'instrucciones_especiales'
        ]
        widgets = {
            'instrucciones_especiales': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tratamiento'].queryset = Tratamiento.objects.filter(activo=True)
        self.fields['medicamento'].queryset = Medicamento.objects.filter(activo=True)

    def clean_cantidad_total(self):
        cant = self.cleaned_data['cantidad_total']
        if cant is None or cant < 1:
            raise ValidationError("La cantidad total debe ser ≥ 1.")
        return cant
