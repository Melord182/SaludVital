from django.contrib import admin
from .models import *
# Register your admin models here.
admin.site.register([SeguroSalud, Especialidad, Paciente, Medico, Medicamento, Tratamiento, ConsultaMedica, RecetaMedica])
