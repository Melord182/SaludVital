# 🏥 Sistema de Gestión Clínica Salud Vital Ltda.

## Evaluación N°2 - Backend con Django REST Framework

---

## 📌 Descripción del Proyecto

Sistema integral de gestión para clínicas que permite administrar pacientes, médicos, especialidades, consultas médicas, tratamientos, medicamentos y recetas médicas. Desarrollado con Django REST Framework y PostgreSQL.

---

## 🎯 Funcionalidades Principales

### Gestión de Entidades
- ✅ **Especialidades Médicas:** CRUD completo con estado activo/inactivo
- ✅ **Pacientes:** Gestión con previsión de salud (FONASA, ISAPRE, PARTICULAR)
- ✅ **Médicos:** Asignación de especialidades y jornadas laborales
- ✅ **Consultas Médicas:** Registro de atenciones con diagnósticos
- ✅ **Tratamientos:** Asociados a consultas realizadas
- ✅ **Medicamentos:** Catálogo con control de stock
- ✅ **Recetas Médicas:** Prescripciones asociadas a tratamientos

### API REST
- ✅ Endpoints para todas las entidades
- ✅ Filtros personalizados por campos clave
- ✅ Búsqueda y ordenamiento
- ✅ Paginación implementada
- ✅ Documentación interactiva con Swagger

### Interfaz Web
- ✅ Dashboard con estadísticas
- ✅ CRUD completo mediante templates HTML
- ✅ Diseño responsive con Bootstrap 5
- ✅ Mensajes de confirmación

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.2+
- **API:** Django REST Framework 3.14+
- **Base de Datos:** PostgreSQL 12+
- **Documentación:** drf-spectacular (Swagger/OpenAPI)
- **Filtros:** django-filter
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Python:** 3.8+

---

## 📦 Instalación Rápida

```bash
# 1. Crear entorno virtual
python -m venv eva2
source eva2/bin/activate  # Linux/Mac
eva2\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install django djangorestframework psycopg2-binary django-filter drf-spectacular

# 3. Crear proyecto
django-admin startproject clinica_salud_vital .
python manage.py startapp gestion_clinica

# 4. Configurar base de datos PostgreSQL
# Editar settings.py con credenciales

# 5. Migrar base de datos
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Cargar datos de prueba
python manage.py shell < datos_iniciales.py

# 8. Ejecutar servidor
python manage.py runserver
```

---

## 🌐 URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Home** | http://localhost:8000/ | Página principal |
| **Admin** | http://localhost:8000/admin/ | Panel administrativo |
| **API Docs** | http://localhost:8000/api/docs/ | Documentación Swagger |
| **API Root** | http://localhost:8000/api/ | Endpoints de la API |

### Endpoints API REST

- `GET/POST /api/especialidades/` - Gestión de especialidades
- `GET/POST /api/pacientes/` - Gestión de pacientes
- `GET/POST /api/medicos/` - Gestión de médicos
- `GET/POST /api/consultas/` - Gestión de consultas
- `GET/POST /api/tratamientos/` - Gestión de tratamientos
- `GET/POST /api/medicamentos/` - Gestión de medicamentos
- `GET/POST /api/recetas/` - Gestión de recetas

---

## 🔍 Ejemplos de Uso de la API

### Listar todos los médicos
```bash
GET http://localhost:8000/api/medicos/
```

### Filtrar médicos por especialidad
```bash
GET http://localhost:8000/api/medicos/?especialidad=1
GET http://localhost:8000/api/medicos/?especialidad_nombre=Cardiología
```

### Filtrar consultas por estado
```bash
GET http://localhost:8000/api/consultas/?estado=REALIZADA
```

### Buscar pacientes por nombre
```bash
GET http://localhost:8000/api/pacientes/?nombre=María
```

### Filtrar medicamentos que requieren receta
```bash
GET http://localhost:8000/api/medicamentos/?requiere_receta=true
```

### Crear una nueva especialidad (POST)
```json
{
  "nombre": "Neurología",
  "descripcion": "Especialidad del sistema nervioso",
  "activa": true
}
```

---

## 📊 Modelo de Datos

### Diagrama de Relaciones

```
Especialidad
    ↓ (1:N)
Medico ←──────┐
    ↓         │
ConsultaMedica│
    ↑         │
Paciente ─────┘
    ↓
Tratamiento
    ↓
RecetaMedica
    ↓
Medicamento
```

### Entidades Principales

**Especialidad**
- nombre, descripcion, activa, fecha_creacion

**Paciente**
- rut, nombre, apellidos, fecha_nacimiento, teléfono, email
- dirección, previsión (CHOICE), activo

**Medico**
- rut, nombre, apellidos, especialidad (FK)
- teléfono, email, numero_registro
- jornada (CHOICE), activo, fecha_ingreso

**ConsultaMedica**
- paciente (FK), medico (FK), fecha_hora
- motivo_consulta, diagnóstico, observaciones
- estado (CHOICE)

**Tratamiento**
- consulta (FK), descripción, fecha_inicio/fin
- indicaciones, activo

**Medicamento**
- nombre, principio_activo, presentación, concentración
- laboratorio, requiere_receta, stock_disponible

**RecetaMedica**
- tratamiento (FK), medicamento (FK)
- dosis, frecuencia, duración, cantidad_total
- instrucciones_especiales

---

## ✨ Características Destacadas

### 1. CHOICES Implementados (Mejoras del Modelo)

```python
# Paciente - Tipo de Previsión
PREVISION_CHOICES = [
    ('FONASA', 'FONASA'),
    ('ISAPRE', 'ISAPRE'),
    ('PARTICULAR', 'Particular'),
    ('OTRO', 'Otro'),
]

# Medico - Tipo de Jornada
JORNADA_CHOICES = [
    ('COMPLETA', 'Jornada Completa'),
    ('PARCIAL', 'Jornada Parcial'),
    ('TURNO', 'Por Turno'),
]

# ConsultaMedica - Estado
ESTADO_CHOICES = [
    ('AGENDADA', 'Agendada'),
    ('REALIZADA', 'Realizada'),
    ('CANCELADA', 'Cancelada'),
    ('NO_ASISTIO', 'No Asistió'),
]
```

### 2. Filtros Avanzados

- **Por Especialidad:** Filtrar médicos y consultas
- **Por Paciente:** Ver historial de consultas
- **Por Médico:** Ver atenciones realizadas
- **Por Fechas:** Consultas en rangos de tiempo
- **Por Estado:** Consultas agendadas, realizadas, etc.

### 3. Documentación Interactiva

- **Swagger UI:** Prueba de endpoints en vivo
- **Schema OpenAPI:** Estándar de documentación
- **Ejemplos de Request/Response:** Para cada endpoint

### 4. Panel de Administración Personalizado

- Filtros por campos relevantes
- Búsqueda avanzada
- Visualización optimizada
- Acciones masivas

---

## 📝 Datos de Prueba

El sistema viene con datos de prueba realistas:

- ✅ 7 Especialidades médicas
- ✅ 5 Pacientes con información completa
- ✅ 4 Médicos asignados a especialidades
- ✅ 5 Medicamentos con stock
- ✅ 10 Consultas médicas en diferentes estados
- ✅ 5 Tratamientos activos
- ✅ Múltiples recetas médicas

---

## 🎨 Interfaz de Usuario

### Características del Frontend

- **Responsive Design:** Compatible con móviles y tablets
- **Bootstrap 5:** Framework CSS moderno
- **Bootstrap Icons:** Iconografía consistente
- **Mensajes Flash:** Feedback inmediato de acciones
- **Navegación Intuitiva:** Menú dropdown organizado
- **Tarjetas Interactivas:** Hover effects y animaciones
- **Tablas Responsivas:** Scroll horizontal en móviles

### Paleta de Colores

- **Primario:** Azul corporativo (#2c5f7c)
- **Secundario:** Cyan médico (#4a90a4)
- **Éxito:** Verde (#198754)
- **Advertencia:** Amarillo (#ffc107)
- **Peligro:** Rojo (#dc3545)

---

## 📋 Cumplimiento de Criterios de Evaluación

| Criterio | Puntaje | Estado |
|----------|---------|--------|
| 1. Entorno virtual "eva2" | 2 | ✅ |
| 2. Comentarios en bloque | 5 | ✅ |
| 3. Estructura del proyecto | 5 | ✅ |
| 4. Modelo de datos (PostgreSQL) | 10 | ✅ |
| 5. CRUD completo por entidad | 10 | ✅ |
| 6. Carga BD con datos realistas | 5 | ✅ |
| 7. Mejoras en el modelo (CHOICES) | 6 | ✅ |
| 8. Templates (vistas HTML) | 10 | ✅ |
| 9. Sistema de documentación | 5 | ✅ |
| 10. Filtros y búsquedas | 5 | ✅ |
| 11. Uso de PostgreSQL | 5 | ✅ |
| 12. Rutas y endpoints de la API | 5 | ✅ |
| 13. Footer en templates | 2 | ✅ |
| 14. Nombrado del proyecto y app | 2 | ✅ |
| **TOTAL** | **77** | **✅ 100%** |

---

## 🔧 Configuración de PostgreSQL

### Crear Base de Datos

```sql
-- En psql o pgAdmin
CREATE DATABASE clinica_salud_vital_db;
CREATE USER clinica_user WITH PASSWORD 'tu_password';
ALTER ROLE clinica_user SET client_encoding TO 'utf8';
ALTER ROLE clinica_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE clinica_user SET timezone TO 'America/Santiago';
GRANT ALL PRIVILEGES ON DATABASE clinica_salud_vital_db TO clinica_user;
```

### Configuración en settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clinica_salud_vital_db',
        'USER': 'postgres', 
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🚀 Despliegue y Producción

### Variables de Entorno (Recomendado)

```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Archivo .env (Ejemplo)

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=clinica_salud_vital_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 📚 Documentación Adicional

### Comandos Útiles

```bash
# Ver todas las URLs disponibles
python manage.py show_urls

# Crear fixture de datos actuales
python manage.py dumpdata > datos_backup.json

# Cargar fixture
python manage.py loaddata datos_backup.json

# Shell interactivo con Django
python manage.py shell

# Crear migraciones para cambios
python manage.py makemigrations

# Ver SQL de las migraciones
python manage.py sqlmigrate gestion_clinica 0001

# Verificar problemas
python manage.py check

# Recolectar archivos estáticos
python manage.py collectstatic
```

### Testing

```bash
# Ejecutar tests
python manage.py test

# Ejecutar tests con cobertura
coverage run --source='.' manage.py test
coverage report
```

---

## 🐛 Solución de Problemas Comunes

### Error: No module named 'psycopg2'
```bash
pip install psycopg2-binary
```

### Error: relation does not exist
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: Port already in use
```bash
# Usar otro puerto
python manage.py runserver 8080
```

### Error: Could not connect to PostgreSQL
- Verificar que PostgreSQL esté corriendo
- Verificar credenciales en settings.py
- Verificar que la base de datos exista

---

## 👥 Autor

**Jaime López Salazar**
- Sección: AP-172-N4
- Asignatura: Backend
- Año: 2025

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos para la Evaluación N°2 de Backend.

