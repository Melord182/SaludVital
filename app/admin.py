from django.contrib import admin
from .models import Especialidad, Paciente, Medico, Medicamento, Consulta_Medica, Tratamiento, Receta_Medica, Tipo_Sangre

# Register your models here.

admin.site.register(Especialidad)
admin.site.register(Paciente)
admin.site.register(Tipo_Sangre)
admin.site.register(Medico)
admin.site.register(Medicamento)
admin.site.register(Consulta_Medica)
admin.site.register(Tratamiento)
admin.site.register(Receta_Medica)
#Aqui se registran los modelos para que aparezcan en el admin de Django, esto nos permite gestionar los datos desde una interfaz web.