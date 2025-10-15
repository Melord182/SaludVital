"""
Archivo: urls.py
Ubicación: Proyecto principal (clinica_salud_vital)

DESCRIPCIÓN GENERAL:
--------------------
Este archivo define las **rutas principales** (URLs) del proyecto Django "clinica_salud_vital".
Su propósito es centralizar y redirigir las distintas URL del sitio hacia:
- El panel de administración de Django.
- Las rutas de la aplicación interna `gestion_clinica`.
- Los endpoints de la documentación de la API generada automáticamente con `drf-spectacular`.

COMPONENTES PRINCIPALES:
------------------------
1. **Admin de Django**  
   - Permite acceder al panel administrativo nativo de Django mediante la ruta `/admin/`.
   - Es útil para gestionar modelos, usuarios y datos del proyecto.

2. **Rutas de la aplicación principal (`gestion_clinica`)**  
   - Incluye las URL definidas dentro del archivo `gestion_clinica/urls.py`.
   - Al colocar `path('', include('gestion_clinica.urls'))`, todas las rutas principales del sitio se manejan desde esa app.

3. **Documentación de la API (DRF Spectacular)**  
   - `SpectacularAPIView`: genera el esquema OpenAPI (en formato JSON o YAML) con la descripción de todos los endpoints.
   - `SpectacularSwaggerView`: crea una interfaz gráfica Swagger UI en `/api/docs/` para visualizar y probar los endpoints REST.
   - Estas herramientas son esenciales para proyectos que exponen una API REST, ya que facilitan la exploración y prueba de los endpoints.

DEPENDENCIAS:
-------------
- `django.contrib.admin`: módulo de administración integrado en Django.
- `django.urls.include` y `django.urls.path`: para declarar y agrupar rutas.
- `drf_spectacular.views`: librería para la generación automática de documentación de APIs (requiere Django REST Framework).

CONCLUSIÓN:
-----------
Este archivo actúa como el punto de entrada de las rutas del proyecto.
A partir de aquí, Django sabe cómo redirigir cada solicitud HTTP al módulo o vista correspondiente.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Administrador de Django
    path('admin/', admin.site.urls),
    
    # URLs de la aplicación gestion_clinica
    path('', include('gestion_clinica.urls')),
    
    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]