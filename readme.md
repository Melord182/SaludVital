# 🏥 Sistema de Gestión Clínica Salud Vital Ltda.

## Tabla de contenidos
- [Descripción general](#descripción-general)
- [Características principales](#características-principales)
- [Tecnologías y dependencias](#tecnologías-y-dependencias)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación y configuración](#instalación-y-configuración)
- [Carga de datos de ejemplo](#carga-de-datos-de-ejemplo)
- [Uso del sistema](#uso-del-sistema)
  - [Interfaz web](#interfaz-web)
  - [API REST](#api-rest)
- [Modelos de datos](#modelos-de-datos)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Pruebas automatizadas](#pruebas-automatizadas)
- [Resolución de problemas frecuentes](#resolución-de-problemas-frecuentes)
- [Próximos pasos sugeridos](#próximos-pasos-sugeridos)

## Descripción general
Aplicación Django orientada a la gestión integral de la clínica Salud Vital Ltda. El proyecto permite administrar pacientes, médicos, especialidades, consultas, tratamientos, medicamentos y recetas, ofreciendo tanto una interfaz web tradicional como una API REST documentada automáticamente con **drf-spectacular**.【F:clinica_salud_vital/settings.py†L20-L125】【F:clinica_salud_vital/urls.py†L40-L54】

## Características principales
- **Cobertura funcional completa** para el flujo clínico: creación y seguimiento de especialidades, fichas de pacientes, agenda médica, tratamientos asociados y recetas farmacológicas.【F:gestion_clinica/models.py†L60-L247】
- **API REST lista para integraciones** con filtros avanzados, búsqueda y ordenamiento por entidad, habilitada a través de `DefaultRouter` y ViewSets de Django REST Framework.【F:gestion_clinica/views.py†L66-L142】【F:gestion_clinica/urls.py†L56-L114】
- **Documentación interactiva** disponible en `/api/docs/` y esquema en `/api/schema/`, generada mediante drf-spectacular para acelerar la exploración de endpoints.【F:clinica_salud_vital/urls.py†L40-L54】
- **Dashboard web** con métricas rápidas y CRUD por cada entidad usando plantillas Django, mensajes de confirmación y manejo seguro de eliminaciones.【F:gestion_clinica/views.py†L145-L200】
- **Script reproducible de datos demo** que limpia la base y crea un set coherente para pruebas manuales o demostraciones.【F:datos_iniciales.py†L7-L200】

## Tecnologías y dependencias
- **Backend:** Django 5.2, Django REST Framework, django-filter, drf-spectacular.【F:requirements.txt†L1-L16】【F:clinica_salud_vital/settings.py†L20-L125】
- **Base de datos:** PostgreSQL (configuración por defecto incluida en `settings.py`).【F:clinica_salud_vital/settings.py†L67-L77】
- **Frontend:** Plantillas Django + archivos estáticos registrados en el proyecto.【F:clinica_salud_vital/settings.py†L49-L103】

## Arquitectura del proyecto
| Módulo | Rol | Detalles |
|--------|-----|----------|
| `clinica_salud_vital/settings.py` | Configuración global | Apps instaladas, PostgreSQL, internacionalización y ajustes de Django REST Framework + drf-spectacular.【F:clinica_salud_vital/settings.py†L20-L125】 |
| `clinica_salud_vital/urls.py` | Enrutamiento raíz | Expone admin, rutas de la app principal y documentación de la API.【F:clinica_salud_vital/urls.py†L40-L54】 |
| `gestion_clinica/models.py` | Dominio clínico | Modelos y relaciones para especialidades, pacientes, médicos, consultas, tratamientos, medicamentos y recetas.【F:gestion_clinica/models.py†L60-L247】 |
| `gestion_clinica/views.py` | Presentación | ViewSets REST y vistas basadas en funciones para dashboard + CRUD web.【F:gestion_clinica/views.py†L62-L200】 |
| `gestion_clinica/filters.py` | Filtros de la API | Declaración de filtros reutilizables por entidad para búsquedas avanzadas.【F:gestion_clinica/filters.py†L56-L157】 |
| `gestion_clinica/urls.py` | Enrutamiento de la app | Monta el router REST en `/api/` y expone rutas HTML por entidad.【F:gestion_clinica/urls.py†L56-L114】 |
| `datos_iniciales.py` | Utilidad de demo | Limpia e inserta datos clínicos de ejemplo en orden seguro.【F:datos_iniciales.py†L7-L200】 |

## Requisitos previos
1. **Python 3.10+** (recomendado Python 3.11 o superior).
2. **PostgreSQL 12+** con una base de datos accesible (por defecto `db_salud_vital` en `localhost:5432`).【F:clinica_salud_vital/settings.py†L67-L77】
3. Herramientas de compilación para instalar `psycopg2-binary` en caso de sistemas basados en Linux.

## Instalación y configuración
1. **Clona el repositorio y crea un entorno virtual**
   ```bash
   git clone <url-del-repo>
   cd SaludVital
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura las credenciales de PostgreSQL**
   - Edita `clinica_salud_vital/settings.py` para apuntar a tu instancia (nombre de base, usuario, contraseña y host).【F:clinica_salud_vital/settings.py†L67-L77】
   - Alternativamente, sobreescribe estos valores usando variables de entorno y un gestor como `python-decouple` (no incluido) según tus estándares.
4. **Ejecuta las migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Crea un superusuario** para acceder al panel admin
   ```bash
   python manage.py createsuperuser
   ```
6. **Levanta el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
7. **Rutas principales en desarrollo**
   - Dashboard web: `http://localhost:8000/`
   - Administración Django: `http://localhost:8000/admin/`
   - Documentación Swagger UI: `http://localhost:8000/api/docs/`

## Carga de datos de ejemplo
1. Asegúrate de trabajar en un entorno de desarrollo: el script eliminará registros existentes de las tablas clínicas.
2. Ejecuta la carga inicial:
   ```bash
   python manage.py shell < datos_iniciales.py
   ```
   - PowerShell: `Get-Content .\datos_iniciales.py | python manage.py shell`
3. El script generará especialidades, pacientes, médicos, medicamentos, consultas, tratamientos y recetas, mostrando un resumen al finalizar.【F:datos_iniciales.py†L7-L200】

## Uso del sistema
### Interfaz web
- Inicio con métricas rápidas: totales de pacientes activos, médicos activos, especialidades disponibles y consultas registradas.【F:gestion_clinica/views.py†L145-L159】
- Formularios CRUD por entidad (`especialidades`, `pacientes`, `medicos`, `consultas`, `tratamientos`, `medicamentos`, `recetas`) con mensajes de confirmación y control de errores comunes como eliminaciones protegidas.【F:gestion_clinica/views.py†L162-L200】

### API REST
- Endpoints disponibles bajo `http://localhost:8000/api/<recurso>/` gracias al router automático de DRF.【F:gestion_clinica/urls.py†L56-L114】
- Funcionalidades clave:
  - **Filtros declarativos** por campos y relaciones (por ejemplo, filtrar consultas por médico, paciente, estado y rango de fechas).【F:gestion_clinica/filters.py†L99-L157】
  - **Búsqueda y ordenamiento** en cada ViewSet mediante `search_fields` y `ordering_fields` (nombres, RUT, especialidad, fechas, etc.).【F:gestion_clinica/views.py†L66-L142】
  - **Paginación estándar** configurable (`PAGE_SIZE=10`).【F:clinica_salud_vital/settings.py†L107-L117】
  - **Documentación interactiva** en `/api/docs/` y esquema en `/api/schema/` generados por drf-spectacular.【F:clinica_salud_vital/urls.py†L40-L54】

## Modelos de datos
| Entidad | Propósito | Atributos destacados |
|---------|-----------|----------------------|
| `Especialidad` | Catálogo de especialidades médicas disponibles. | Nombre único, descripción, estado activo.【F:gestion_clinica/models.py†L60-L76】 |
| `Paciente` | Ficha de pacientes con datos personales y previsión. | RUT único, contacto, previsión con `choices`, estado activo.【F:gestion_clinica/models.py†L78-L114】 |
| `Medico` | Profesionales asociados a especialidades. | Registro colegiado, jornada laboral, relación `ForeignKey` a especialidad.【F:gestion_clinica/models.py†L116-L151】 |
| `ConsultaMedica` | Citas que relacionan paciente y médico. | Fecha/hora, motivo, diagnóstico, estado con `choices` y seguimiento temporal.【F:gestion_clinica/models.py†L153-L181】 |
| `Medicamento` | Inventario de fármacos. | Presentación, concentración, laboratorio, bandera `requiere_receta`, stock con validador mínimo.【F:gestion_clinica/models.py†L184-L205】 |
| `Tratamiento` | Indicaciones derivadas de una consulta. | Rango de fechas, descripción, relación con consulta y estado activo.【F:gestion_clinica/models.py†L207-L224】 |
| `RecetaMedica` | Recetas asociadas a un tratamiento y medicamento. | Dosis, frecuencia, duración, cantidad total con validador mínimo y fecha de emisión automática.【F:gestion_clinica/models.py†L227-L247】 |

## Estructura del repositorio
```text
SaludVital/
├── clinica_salud_vital/      # Configuración del proyecto y URLs raíz
├── gestion_clinica/          # Aplicación principal: modelos, vistas, filtros, serializers
├── templates/                # Plantillas HTML para la interfaz web
├── static/                   # Archivos estáticos (CSS, JS, imágenes)
├── datos_iniciales.py        # Script de carga de datos demo
├── manage.py                 # Punto de entrada de comandos Django
└── requirements.txt          # Dependencias del entorno
```
Los directorios `templates` y `static` están declarados en la configuración para su uso en desarrollo/producción.【F:clinica_salud_vital/settings.py†L49-L103】

## Pruebas automatizadas
Ejecuta la suite de tests (extiende `gestion_clinica/tests.py` con tus casos):
```bash
python manage.py test
```
Se incluye una plantilla básica lista para ser ampliada con pruebas unitarias e integraciones específicas.【F:gestion_clinica/tests.py†L1-L3】

## Resolución de problemas frecuentes
- **Error de conexión a PostgreSQL:** verifica credenciales, host y puerto; ajusta la sección `DATABASES` según tu entorno.【F:clinica_salud_vital/settings.py†L67-L77】
- **No se ven datos de ejemplo:** vuelve a ejecutar `datos_iniciales.py` en una base limpia o restablece manualmente las tablas afectadas.【F:datos_iniciales.py†L76-L200】
- **Filtros sin resultados:** revisa los parámetros (`?nombre=`, `?especialidad=`, `?fecha_desde=`) y la paginación (`?page=`) aplicados por DRF.【F:gestion_clinica/filters.py†L56-L157】【F:clinica_salud_vital/settings.py†L107-L117】

## Próximos pasos sugeridos
- Añadir autenticación y permisos a la API (`IsAuthenticated`, tokens o JWT).
- Sustituir formularios manuales por `ModelForm` para validaciones más completas.
- Implementar pruebas unitarias y de integración que cubran el flujo clínico completo.
- Configurar despliegue automatizado (Docker, CI/CD, infraestructura como código) acorde al entorno objetivo.

---
**Autor original:** Jaime López Salazar — Proyecto académico para la asignatura de Backend.
