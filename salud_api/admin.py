from django.contrib import admin
from .models import Especialidad, Paciente, Medico, Medicamento, Consulta_Medica, Tratamiento, Receta_Medica, Tipo_Sangre, Usuario, Laboratorio


admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Medicamento)
admin.site.register(Laboratorio)
admin.site.register(Consulta_Medica)
admin.site.register(Tratamiento)
admin.site.register(Receta_Medica)
admin.site.register(Tipo_Sangre)
admin.site.register(Usuario)

# Register your models here.

