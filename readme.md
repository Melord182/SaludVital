# 🏥 Sistema de Gestión Clínica Salud Vital Ltda.

## Tabla de contenidos
- [Descripción general](#descripción-general)
- [Funcionalidades clave](#funcionalidades-clave)
- [Arquitectura y módulos principales](#arquitectura-y-módulos-principales)
- [Requisitos y dependencias](#requisitos-y-dependencias)
- [Guía de instalación y configuración](#guía-de-instalación-y-configuración)
- [Carga de datos de ejemplo](#carga-de-datos-de-ejemplo)
- [Uso del sistema](#uso-del-sistema)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Resolución de problemas frecuentes](#resolución-de-problemas-frecuentes)

## Descripción general
Sistema integral para administrar la operación diaria de la clínica Salud Vital Ltda. Incluye gestión de pacientes, médicos, consultas, tratamientos, medicamentos y recetas, exponiendo tanto una interfaz web tradicional como una API REST totalmente documentada. La configuración del proyecto habilita Django REST Framework, filtros, paginación y documentación automática con drf-spectacular para ofrecer una experiencia moderna de integración. 【F:clinica_salud_vital/settings.py†L20-L125】【F:clinica_salud_vital/urls.py†L44-L54】

## Funcionalidades clave
- **Modelado clínico completo**: entidades para especialidades, pacientes, médicos, consultas médicas, tratamientos, medicamentos y recetas con relaciones y validaciones pensadas para entornos asistenciales. 【F:gestion_clinica/models.py†L60-L200】
- **API REST lista para producción**: ViewSets con búsqueda, ordenamiento y filtros personalizados para cada entidad, ideales para integraciones externas o SPA. 【F:gestion_clinica/views.py†L61-L142】【F:gestion_clinica/filters.py†L33-L142】
- **Interfaz web administrativa**: vistas basadas en templates que cubren operaciones CRUD por entidad y un dashboard con métricas generales. 【F:gestion_clinica/views.py†L148-L200】
- **Documentación interactiva**: esquema OpenAPI y Swagger UI disponibles en `/api/schema/` y `/api/docs/`. 【F:clinica_salud_vital/urls.py†L51-L54】
- **Datos demo reproducibles**: script de carga que limpia la base y genera un set coherente de información clínica para pruebas manuales o demostraciones. 【F:datos_iniciales.py†L1-L170】

## Arquitectura y módulos principales
| Módulo | Descripción |
|--------|-------------|
| `clinica_salud_vital/settings.py` | Configuración global: apps instaladas, DRF (filtros, paginación, esquema), integración con drf-spectacular y rutas de estáticos. 【F:clinica_salud_vital/settings.py†L20-L125】 |
| `clinica_salud_vital/urls.py` | Punto de entrada de URLs, expone admin, aplicación principal y documentación de la API. 【F:clinica_salud_vital/urls.py†L44-L54】 |
| `gestion_clinica/models.py` | Define el dominio clínico completo con relaciones, choices y propiedades auxiliares. 【F:gestion_clinica/models.py†L60-L200】 |
| `gestion_clinica/views.py` | Contiene los ViewSets DRF y las vistas web (dashboard + CRUD) que reutilizan filtros y serializadores. 【F:gestion_clinica/views.py†L61-L200】 |
| `gestion_clinica/filters.py` | Filtros avanzados por campo, rango, relaciones y estados para cada entidad. 【F:gestion_clinica/filters.py†L33-L142】 |
| `datos_iniciales.py` | Script utilitario para limpiar y poblar datos de ejemplo en orden seguro. 【F:datos_iniciales.py†L7-L170】 |

## Requisitos y dependencias
- Python 3.10 o superior (recomendado para Django 5.2).
- PostgreSQL 12 o superior.
- Dependencias Python clave:
  - Django 5.2.7.
  - Django REST Framework 3.16.1.
  - django-filter 25.2.
  - drf-spectacular 0.28.0.
  - psycopg2-binary 2.9.11 para la conexión con PostgreSQL. 【F:requirements.txt†L3-L11】

## Guía de instalación y configuración
1. **Clonar el repositorio y crear un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar variables de entorno**
   - Define `DJANGO_SECRET_KEY`, `DEBUG` y las credenciales de base de datos antes de desplegar.
   - Actualiza `DATABASES` o usa variables de entorno para apuntar a la instancia deseada (por defecto se usa PostgreSQL local `db_salud_vital`). 【F:clinica_salud_vital/settings.py†L67-L77】
4. **Aplicar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Crear un superusuario para el admin**
   ```bash
   python manage.py createsuperuser
   ```
6. **Levantar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
7. **Accesos principales**
   - Home / dashboard: `http://localhost:8000/`
   - Admin de Django: `http://localhost:8000/admin/`
   - Documentación Swagger UI: `http://localhost:8000/api/docs/`

## Carga de datos de ejemplo
1. Verifica que la base esté vacía o que se trate de un entorno de desarrollo (el script elimina registros existentes en las tablas clínicas).
2. Ejecuta el script de datos iniciales:
   ```bash
   python manage.py shell < datos_iniciales.py
   ```
   - En PowerShell usa `Get-Content .\datos_iniciales.py | python manage.py shell`.
3. El script creará especialidades, pacientes, médicos, medicamentos, consultas, tratamientos y recetas en orden seguro e imprimirá un resumen final. 【F:datos_iniciales.py†L11-L170】

## Uso del sistema
### Interfaz web
- Navega por los menús `especialidades`, `pacientes`, `médicos`, `consultas`, `tratamientos`, `medicamentos` y `recetas` para gestionar registros mediante formularios HTML.
- El home muestra totales de pacientes, médicos, especialidades activas y consultas registradas. 【F:gestion_clinica/views.py†L148-L170】

### API REST
- Endpoints base disponibles en `/api/<recurso>/` gracias al router de Django REST Framework. 【F:gestion_clinica/urls.py†L56-L114】
- Filtros y parámetros comunes:
  - Búsqueda por nombre, apellidos o RUT en pacientes y médicos (`search` + filtros personalizados). 【F:gestion_clinica/views.py†L76-L107】【F:gestion_clinica/filters.py†L49-L85】
  - Filtrado por especialidad, estado de consulta, fecha desde/hasta y más. 【F:gestion_clinica/views.py†L87-L142】【F:gestion_clinica/filters.py†L87-L142】
  - Paginación estándar con tamaño de página 10 configurable. 【F:clinica_salud_vital/settings.py†L107-L117】
- Documentación interactiva en `/api/docs/` y esquema en `/api/schema/` para explorar y probar cada endpoint. 【F:clinica_salud_vital/urls.py†L51-L54】

## Pruebas y calidad
- Ejecuta los tests definidos en la aplicación con:
  ```bash
  python manage.py test
  ```
  (Se proporciona una plantilla inicial en `gestion_clinica/tests.py` para extender las pruebas unitarias y de integración). 【F:gestion_clinica/tests.py†L1-L3】

## Estructura del proyecto
```
SaludVital/
├── clinica_salud_vital/      # Configuración del proyecto y URLs raíz
├── gestion_clinica/          # Aplicación principal (modelos, vistas, filtros, serializers)
├── templates/                # Plantillas HTML para la interfaz web
├── static/                   # Archivos estáticos gestionados por Django
├── datos_iniciales.py        # Script de carga de datos demo
├── manage.py                 # Punto de entrada de comandos Django
└── requirements.txt          # Dependencias del entorno
```
Los directorios `templates` y `static` están registrados en la configuración para su uso en producción/desarrollo. 【F:clinica_salud_vital/settings.py†L49-L103】

## Resolución de problemas frecuentes
- **Error de conexión a PostgreSQL**: confirma credenciales, puerto y disponibilidad del servicio; ajusta `DATABASES` en `settings.py` o variables de entorno. 【F:clinica_salud_vital/settings.py†L67-L77】
- **Falta de datos para pruebas**: vuelve a ejecutar `datos_iniciales.py` en un entorno de desarrollo limpio. 【F:datos_iniciales.py†L11-L170】
- **Resultados vacíos en la API**: revisa los parámetros de filtro (`?nombre=`, `?especialidad=`, `?fecha_desde=`) y la paginación (`?page=`). 【F:gestion_clinica/filters.py†L49-L142】【F:clinica_salud_vital/settings.py†L107-L117】

---
**Autor original:** Jaime López Salazar — Proyecto académico para la asignatura de Backend.
