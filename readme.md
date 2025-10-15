# 🏥 Sistema de Gestión Clínica Salud Vital Ltda.

Guía rápida para instalar, configurar y comprender la arquitectura del proyecto académico **Salud Vital** construido con Django y Django REST Framework.

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

El sistema cubre la operación diaria de la clínica: registro de pacientes, profesionales, consultas, tratamientos, medicamentos y recetas. Ofrece una interfaz web tradicional para la gestión interna y una API REST con documentación automática para integraciones externas.

## Funcionalidades clave

- **Modelado clínico completo**: incluye especialidades, pacientes, médicos, consultas, tratamientos, medicamentos y recetas con validaciones y relaciones entre entidades.
- **API REST lista para producción**: expuesta mediante ViewSets de Django REST Framework con paginación, búsqueda y filtros avanzados.
- **Interfaz web administrativa**: plantillas HTML para gestionar cada entidad y un dashboard con indicadores generales.
- **Documentación interactiva**: OpenAPI Schema y Swagger UI disponibles en `/api/schema/` y `/api/docs/`.
- **Datos demo reproducibles**: script de carga que genera un conjunto coherente de datos para pruebas manuales.

## Arquitectura y módulos principales

| Módulo | Descripción |
|--------|-------------|
| `clinica_salud_vital/settings.py` | Configuración global de Django, inclusión de apps, DRF (filtros, paginación, esquema) y drf-spectacular. |
| `clinica_salud_vital/urls.py` | Registro de rutas: admin, aplicación principal y documentación de la API. |
| `gestion_clinica/models.py` | Definición del dominio clínico con relaciones y métodos auxiliares. |
| `gestion_clinica/views.py` | ViewSets REST y vistas basadas en plantillas para el dashboard y CRUD. |
| `gestion_clinica/filters.py` | Conjunto de filtros por campos, rangos y relaciones para cada entidad. |
| `gestion_clinica/serializers.py` | Serializadores DRF que encapsulan reglas de validación y representación. |
| `datos_iniciales.py` | Script utilitario para limpiar y poblar datos de ejemplo en orden seguro. |

## Requisitos y dependencias

- Python 3.10 o superior (recomendado para Django 5.2).
- PostgreSQL 12 o superior.
- Dependencias principales del archivo `requirements.txt`:
  - Django 5.2.7
  - Django REST Framework 3.16.1
  - django-filter 25.2
  - drf-spectacular 0.28.0
  - psycopg2-binary 2.9.11

## Guía de instalación y configuración

1. **Crear y activar un entorno virtual**
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
   - Define `DJANGO_SECRET_KEY`, `DEBUG` y las credenciales de base de datos.
   - Ajusta la configuración de `DATABASES` o utiliza variables de entorno para apuntar a tu instancia de PostgreSQL (por defecto `db_salud_vital`).
4. **Aplicar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Crear un superusuario**
   ```bash
   python manage.py createsuperuser
   ```
6. **Levantar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
7. **Accesos principales**
   - Dashboard: `http://localhost:8000/`
   - Admin de Django: `http://localhost:8000/admin/`
   - Documentación Swagger UI: `http://localhost:8000/api/docs/`

## Carga de datos de ejemplo

1. Asegúrate de trabajar en una base de datos vacía o de desarrollo (el script elimina registros clínicos previos).
2. Ejecuta el script de carga:
   ```bash
   python manage.py shell < datos_iniciales.py
   ```
   - En PowerShell: `Get-Content .\datos_iniciales.py | python manage.py shell`
3. Se crearán especialidades, pacientes, médicos, medicamentos, consultas, tratamientos y recetas con relaciones consistentes.

## Uso del sistema

### Interfaz web
- Usa los menús de la barra superior para gestionar especialidades, pacientes, médicos, consultas, tratamientos, medicamentos y recetas.
- El inicio muestra indicadores globales como conteo de pacientes, médicos, especialidades activas y consultas registradas.

### API REST
- Endpoints base disponibles en `/api/<recurso>/` mediante el router de DRF.
- Parámetros comunes:
  - `search`: búsqueda por nombre, apellidos o RUT en pacientes y médicos.
  - Filtros por especialidad, estado de consulta y rangos de fechas.
  - Paginación estándar (10 elementos por página por defecto).
- Explora la API desde `/api/docs/` o descarga el esquema desde `/api/schema/`.

## Pruebas y calidad

Ejecuta la suite de pruebas con:
```bash
python manage.py test
```
El módulo `gestion_clinica/tests.py` contiene la estructura base para ampliar casos unitarios e integraciones.

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

## Resolución de problemas frecuentes

- **Error de conexión a PostgreSQL**: revisa credenciales, puerto y disponibilidad del servicio; actualiza `DATABASES` o las variables de entorno asociadas.
- **Falta de datos para pruebas**: vuelve a ejecutar `datos_iniciales.py` en una base de desarrollo limpia.
- **Resultados vacíos en la API**: verifica parámetros de filtrado (`?nombre=`, `?especialidad=`, `?fecha_desde=`) y la paginación (`?page=`).

---
**Autor original:** Jaime López Salazar — Proyecto académico para la asignatura de Backend.
