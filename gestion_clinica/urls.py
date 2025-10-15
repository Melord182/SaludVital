"""
Archivo: urls.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este archivo define las **rutas (URLs)** correspondientes a la aplicación `gestion_clinica`, 
tanto para la parte **web (templates CRUD)** como para la **API REST**.

Su función es conectar las peticiones del usuario con las vistas adecuadas (funciones o viewsets),
permitiendo una navegación clara en el sitio y una interacción estructurada con los recursos de la API.

ESTRUCTURA DEL ARCHIVO:
-----------------------
1️⃣ **Router de la API REST (Django REST Framework)**  
   - Usa `DefaultRouter` para registrar los *ViewSets* de cada modelo.
   - Cada `router.register()` crea automáticamente las rutas estándar REST:
     - `GET /api/modelo/` → Lista de registros.  
     - `GET /api/modelo/{id}/` → Detalle de un registro.  
     - `POST /api/modelo/` → Crear registro.  
     - `PUT /api/modelo/{id}/` → Actualizar registro.  
     - `DELETE /api/modelo/{id}/` → Eliminar registro.
   - Esto permite gestionar fácilmente los datos de forma programática desde el frontend o clientes externos.

2️⃣ **Rutas HTML (Templates CRUD)**  
   - Se definen con `path()` y apuntan a vistas que renderizan páginas HTML.
   - Cada entidad (Paciente, Médico, Consulta, etc.) cuenta con sus operaciones CRUD:
     - `listar`, `crear`, `editar` y `eliminar`.
   - Estas vistas están pensadas para la administración interna vía interfaz web (no API).

3️⃣ **Página principal (`home`)**  
   - Actúa como punto de entrada de la aplicación (vista inicial del sistema clínico).

INTEGRACIÓN CON LA API REST:
----------------------------
✔ El router DRF se monta en la ruta `/api/`.  
✔ Todos los endpoints se documentan automáticamente en Swagger (`/api/docs/`).  
✔ Las rutas CRUD HTML coexisten con los endpoints REST sin interferencias.  

DEPENDENCIAS:
-------------
- `django.urls.path` y `include`: para definir y agrupar rutas.
- `rest_framework.routers.DefaultRouter`: genera automáticamente las rutas REST.
- `.views`: contiene las vistas funcionales y los viewsets asociados.

CONCLUSIÓN:
-----------
Este archivo es el **núcleo de enrutamiento de la aplicación**, unificando tanto la interfaz web (templates)
como los servicios API, garantizando que cada operación sobre los modelos clínicos esté correctamente expuesta.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para la API REST
router = DefaultRouter()
router.register(r'especialidades', views.EspecialidadViewSet, basename='especialidad-api')
router.register(r'pacientes', views.PacienteViewSet, basename='paciente-api')
router.register(r'medicos', views.MedicoViewSet, basename='medico-api')
router.register(r'consultas', views.ConsultaMedicaViewSet, basename='consulta-api')
router.register(r'tratamientos', views.TratamientoViewSet, basename='tratamiento-api')
router.register(r'medicamentos', views.MedicamentoViewSet, basename='medicamento-api')
router.register(r'recetas', views.RecetaMedicaViewSet, basename='receta-api')

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),
    
    # URLs de la API REST
    path('api/', include(router.urls)),
    
    # URLs para CRUD de Especialidad
    path('especialidades/', views.especialidad_lista, name='especialidad_lista'),
    path('especialidades/crear/', views.especialidad_crear, name='especialidad_crear'),
    path('especialidades/<int:pk>/editar/', views.especialidad_editar, name='especialidad_editar'),
    path('especialidades/<int:pk>/eliminar/', views.especialidad_eliminar, name='especialidad_eliminar'),
    
    # URLs para CRUD de Paciente
    path('pacientes/', views.paciente_lista, name='paciente_lista'),
    path('pacientes/crear/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/<int:pk>/editar/', views.paciente_editar, name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),
    
    # URLs para CRUD de Médico
    path('medicos/', views.medico_lista, name='medico_lista'),
    path('medicos/crear/', views.medico_crear, name='medico_crear'),
    path('medicos/<int:pk>/editar/', views.medico_editar, name='medico_editar'),
    path('medicos/<int:pk>/eliminar/', views.medico_eliminar, name='medico_eliminar'),
    
    # URLs para CRUD de Consulta Médica
    path('consultas/', views.consulta_lista, name='consulta_lista'),
    path('consultas/crear/', views.consulta_crear, name='consulta_crear'),
    path('consultas/<int:pk>/editar/', views.consulta_editar, name='consulta_editar'),
    path('consultas/<int:pk>/eliminar/', views.consulta_eliminar, name='consulta_eliminar'),
    
    # URLs para CRUD de Tratamiento
    path('tratamientos/', views.tratamiento_lista, name='tratamiento_lista'),
    path('tratamientos/crear/', views.tratamiento_crear, name='tratamiento_crear'),
    path('tratamientos/<int:pk>/editar/', views.tratamiento_editar, name='tratamiento_editar'),
    path('tratamientos/<int:pk>/eliminar/', views.tratamiento_eliminar, name='tratamiento_eliminar'),
    
    # URLs para CRUD de Medicamento
    path('medicamentos/', views.medicamento_lista, name='medicamento_lista'),
    path('medicamentos/crear/', views.medicamento_crear, name='medicamento_crear'),
    path('medicamentos/<int:pk>/editar/', views.medicamento_editar, name='medicamento_editar'),
    path('medicamentos/<int:pk>/eliminar/', views.medicamento_eliminar, name='medicamento_eliminar'),
    
    # URLs para CRUD de Receta Médica
    path('recetas/', views.receta_lista, name='receta_lista'),
    path('recetas/crear/', views.receta_crear, name='receta_crear'),
    path('recetas/<int:pk>/editar/', views.receta_editar, name='receta_editar'),
    path('recetas/<int:pk>/eliminar/', views.receta_eliminar, name='receta_eliminar'),
]