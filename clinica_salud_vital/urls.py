"""
Configuración de URLs para el proyecto clinica_salud_vital.
Define las rutas principales, admin, API y documentación.
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