"""
Archivo: datos_iniciales.py
Ubicación: Raíz del proyecto o dentro de la app (según tu preferencia)

DESCRIPCIÓN GENERAL:
--------------------
Este script **puebla la base de datos con datos realistas** para el sistema de gestión de clínica.
Crea entidades en un orden coherente (Especialidades → Pacientes → Médicos → Medicamentos → Consultas → Tratamientos → Recetas)
y, antes de eso, **limpia** tablas dependientes para evitar conflictos de integridad referencial.

QUÉ HACE PASO A PASO:
---------------------
1) **Limpieza (opcional)**  
   - Elimina en orden seguro: Recetas → Tratamientos → Consultas → Médicos → Pacientes → Medicamentos → Especialidades.
   - Útil para rehacer escenarios de prueba desde cero.

2) **Catálogo base**  
   - Crea 7 **Especialidades** activas.

3) **Personas**  
   - Inserta 5 **Pacientes** con RUT, contacto, previsión y estado activo.
   - Inserta 4 **Médicos** asignando especialidad en forma circular (round-robin), con jornada y registro.

4) **Inventario**  
   - Inserta 5 **Medicamentos** con presentación, concentración, laboratorio, receta requerida y stock.

5) **Actividad clínica**  
   - Genera 10 **Consultas** con fechas recientes (1 a 60 días atrás), estado aleatorio y textos de motivo/diagnóstico.
   - Para consultas **REALIZADAS**, crea **Tratamientos** (máx. 5), con fecha de inicio/fin e indicaciones.
   - Para cada tratamiento, genera de 1 a 3 **Recetas** con dosis, frecuencia, duración y cantidad total.

6) **Resumen**  
   - Imprime un resumen con totales creados por entidad.

CÓMO EJECUTARLO:
----------------
- **Bash / CMD (Windows cmd.exe):**
    python manage.py shell < datos_iniciales.py

- **PowerShell (evita el error del operador '<')**:
    Get-Content .\datos_iniciales.py | python manage.py shell
  (Alternativa: `type .\datos_iniciales.py | python manage.py shell` en cmd.exe)

- **Shell interactivo (opción)**:
    python manage.py shell
    >>> exec(open("datos_iniciales.py", encoding="utf-8").read())

NOTAS Y BUENAS PRÁCTICAS:
-------------------------
- **Aleatoriedad**: se usa `random` para distribuir fechas/estados/recetas. Si necesitas reproducibilidad exacta,
  fija una semilla al inicio: `random.seed(42)`.
- **Zonas horarias**: para proyectos con `USE_TZ=True`, considera usar `timezone.now()` en lugar de `datetime.now()`.
- **Desempeño**: para cargas masivas, podrías migrar a `bulk_create` por entidad.
- **Idempotencia**: la limpieza inicial permite ejecutar el script múltiples veces sin duplicar datos.
- **Seguridad**: ¡Ojo! la limpieza borra datos existentes de esas tablas. Úsalo solo en entornos de desarrollo/prueba.

DEPENDENCIAS:
-------------
- Modelos de la app `gestion_clinica`.
- Módulos estándar: `datetime`, `random`.

RESULTADO ESPERADO:
-------------------
Una base de datos de desarrollo **lista para pruebas** de vistas, admin y API, con relaciones consistentes
y variedad suficiente de estados clínicos para validar filtros, búsquedas y paginación.
"""
from gestion_clinica.models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica
)
from datetime import date, datetime, timedelta
import random

print("Iniciando carga de datos...")

# Limpiar datos existentes (opcional)
RecetaMedica.objects.all().delete()
Tratamiento.objects.all().delete()
ConsultaMedica.objects.all().delete()
Medico.objects.all().delete()
Paciente.objects.all().delete()
Medicamento.objects.all().delete()
Especialidad.objects.all().delete()

print("Datos anteriores eliminados.")

# 1. Crear Especialidades
especialidades_data = [
    {"nombre": "Cardiología", "descripcion": "Especialidad médica que se ocupa del corazón y sistema circulatorio"},
    {"nombre": "Pediatría", "descripcion": "Medicina dedicada al cuidado de niños y adolescentes"},
    {"nombre": "Traumatología", "descripcion": "Tratamiento de lesiones del sistema musculoesquelético"},
    {"nombre": "Medicina General", "descripcion": "Atención médica integral y preventiva"},
    {"nombre": "Ginecología", "descripcion": "Especialidad enfocada en la salud femenina"},
    {"nombre": "Dermatología", "descripcion": "Tratamiento de enfermedades de la piel"},
    {"nombre": "Oftalmología", "descripcion": "Especialidad dedicada al cuidado de los ojos"},
]

especialidades = []
for esp_data in especialidades_data:
    especialidad = Especialidad.objects.create(**esp_data, activa=True)
    especialidades.append(especialidad)
    print(f"✓ Especialidad creada: {especialidad.nombre}")

# 2. Crear Pacientes
pacientes_data = [
    {"rut": "12345678-9", "nombre": "María", "apellido_paterno": "González", "apellido_materno": "López", 
     "fecha_nacimiento": date(1985, 3, 15), "telefono": "+56912345678", "email": "maria.gonzalez@email.com",
     "direccion": "Av. Libertador 1234, Santiago", "prevision": "FONASA"},
    {"rut": "23456789-0", "nombre": "Juan", "apellido_paterno": "Pérez", "apellido_materno": "Soto",
     "fecha_nacimiento": date(1990, 7, 22), "telefono": "+56923456789", "email": "juan.perez@email.com",
     "direccion": "Calle Principal 567, Providencia", "prevision": "ISAPRE"},
    {"rut": "34567890-1", "nombre": "Ana", "apellido_paterno": "Martínez", "apellido_materno": "Rojas",
     "fecha_nacimiento": date(1978, 11, 8), "telefono": "+56934567890", "email": "ana.martinez@email.com",
     "direccion": "Pasaje Los Robles 890, Las Condes", "prevision": "FONASA"},
    {"rut": "45678901-2", "nombre": "Carlos", "apellido_paterno": "Silva", "apellido_materno": "Vargas",
     "fecha_nacimiento": date(1995, 5, 30), "telefono": "+56945678901", "email": "carlos.silva@email.com",
     "direccion": "Av. Apoquindo 2345, Las Condes", "prevision": "PARTICULAR"},
    {"rut": "56789012-3", "nombre": "Patricia", "apellido_paterno": "Fernández", "apellido_materno": "Muñoz",
     "fecha_nacimiento": date(1982, 9, 12), "telefono": "+56956789012", "email": "patricia.fernandez@email.com",
     "direccion": "Calle Los Pinos 456, Ñuñoa", "prevision": "ISAPRE"},
]

pacientes = []
for pac_data in pacientes_data:
    paciente = Paciente.objects.create(**pac_data, activo=True)
    pacientes.append(paciente)
    print(f"✓ Paciente creado: {paciente.nombre_completo}")

# 3. Crear Médicos
medicos_data = [
    {"rut": "11111111-1", "nombre": "Roberto", "apellido_paterno": "Carrasco", "apellido_materno": "Torres",
     "telefono": "+56911111111", "email": "r.carrasco@clinica.cl", "numero_registro": "REG-001",
     "fecha_ingreso": date(2015, 1, 10), "jornada": "COMPLETA"},
    {"rut": "22222222-2", "nombre": "Laura", "apellido_paterno": "Ramírez", "apellido_materno": "Núñez",
     "telefono": "+56922222222", "email": "l.ramirez@clinica.cl", "numero_registro": "REG-002",
     "fecha_ingreso": date(2018, 5, 20), "jornada": "COMPLETA"},
    {"rut": "33333333-3", "nombre": "Diego", "apellido_paterno": "Morales", "apellido_materno": "Castro",
     "telefono": "+56933333333", "email": "d.morales@clinica.cl", "numero_registro": "REG-003",
     "fecha_ingreso": date(2020, 3, 15), "jornada": "PARCIAL"},
    {"rut": "44444444-4", "nombre": "Carmen", "apellido_paterno": "Vega", "apellido_materno": "Bravo",
     "telefono": "+56944444444", "email": "c.vega@clinica.cl", "numero_registro": "REG-004",
     "fecha_ingreso": date(2017, 9, 1), "jornada": "COMPLETA"},
]

medicos = []
for i, med_data in enumerate(medicos_data):
    especialidad = especialidades[i % len(especialidades)]
    medico = Medico.objects.create(**med_data, especialidad=especialidad, activo=True)
    medicos.append(medico)
    print(f"✓ Médico creado: {medico.nombre_completo} - {especialidad.nombre}")

# 4. Crear Medicamentos
medicamentos_data = [
    {"nombre": "Paracetamol", "principio_activo": "Paracetamol", "presentacion": "Tabletas",
     "concentracion": "500mg", "laboratorio": "Laboratorio Chile", "requiere_receta": False, "stock_disponible": 500},
    {"nombre": "Ibuprofeno", "principio_activo": "Ibuprofeno", "presentacion": "Cápsulas",
     "concentracion": "400mg", "laboratorio": "Farma Plus", "requiere_receta": False, "stock_disponible": 300},
    {"nombre": "Amoxicilina", "principio_activo": "Amoxicilina", "presentacion": "Cápsulas",
     "concentracion": "500mg", "laboratorio": "Antibióticos S.A.", "requiere_receta": True, "stock_disponible": 200},
    {"nombre": "Losartán", "principio_activo": "Losartán", "presentacion": "Tabletas",
     "concentracion": "50mg", "laboratorio": "CardioMed", "requiere_receta": True, "stock_disponible": 150},
    {"nombre": "Omeprazol", "principio_activo": "Omeprazol", "presentacion": "Cápsulas",
     "concentracion": "20mg", "laboratorio": "Gastro Lab", "requiere_receta": False, "stock_disponible": 250},
]

medicamentos = []
for med_data in medicamentos_data:
    medicamento = Medicamento.objects.create(**med_data, activo=True)
    medicamentos.append(medicamento)
    print(f"✓ Medicamento creado: {medicamento.nombre}")

# 5. Crear Consultas Médicas
consultas = []
estados = ['AGENDADA', 'REALIZADA', 'CANCELADA', 'NO_ASISTIO']
motivos = [
    "Dolor abdominal persistente",
    "Control de presión arterial",
    "Dolor de cabeza frecuente",
    "Control pediátrico rutinario",
    "Dolor en articulaciones",
    "Chequeo general de salud",
    "Problemas respiratorios",
]

for i in range(10):
    fecha_hora = datetime.now() - timedelta(days=random.randint(1, 60))
    paciente = random.choice(pacientes)
    medico = random.choice(medicos)
    estado = random.choice(estados)
    
    consulta = ConsultaMedica.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_hora=fecha_hora,
        motivo_consulta=random.choice(motivos),
        diagnostico="Diagnóstico médico según evaluación clínica." if estado == 'REALIZADA' else "",
        observaciones="Paciente estable, seguir indicaciones." if estado == 'REALIZADA' else "",
        estado=estado
    )
    consultas.append(consulta)
    print(f"✓ Consulta creada: {consulta.id} - {paciente.nombre} con Dr(a). {medico.apellido_paterno}")

# 6. Crear Tratamientos (solo para consultas realizadas)
tratamientos = []
consultas_realizadas = [c for c in consultas if c.estado == 'REALIZADA']

for consulta in consultas_realizadas[:5]:
    fecha_inicio = consulta.fecha_hora.date()
    fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 30))
    
    tratamiento = Tratamiento.objects.create(
        consulta=consulta,
        descripcion=f"Tratamiento médico para {consulta.motivo_consulta.lower()}",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        indicaciones="Reposo relativo. Tomar medicación según indicaciones. Control en 15 días.",
        activo=True
    )
    tratamientos.append(tratamiento)
    print(f"✓ Tratamiento creado: {tratamiento.id} - Consulta {consulta.id}")

# 7. Crear Recetas Médicas
recetas = []
dosis_opciones = ["1 tableta", "2 tabletas", "1 cápsula", "2 cápsulas"]
frecuencia_opciones = ["Cada 8 horas", "Cada 12 horas", "Una vez al día", "Dos veces al día"]
duracion_opciones = ["7 días", "10 días", "14 días", "30 días"]

for tratamiento in tratamientos:
    num_medicamentos = random.randint(1, 3)
    medicamentos_receta = random.sample(medicamentos, num_medicamentos)
    
    for medicamento in medicamentos_receta:
        receta = RecetaMedica.objects.create(
            tratamiento=tratamiento,
            medicamento=medicamento,
            dosis=random.choice(dosis_opciones),
            frecuencia=random.choice(frecuencia_opciones),
            duracion=random.choice(duracion_opciones),
            cantidad_total=random.randint(10, 60),
            instrucciones_especiales="Tomar con alimentos. Evitar alcohol durante el tratamiento."
        )
        recetas.append(receta)
        print(f"✓ Receta creada: {receta.id} - {medicamento.nombre}")

print("\n" + "="*50)
print("RESUMEN DE DATOS CARGADOS")
print("="*50)
print(f"✓ Especialidades: {len(especialidades)}")
print(f"✓ Pacientes: {len(pacientes)}")
print(f"✓ Médicos: {len(medicos)}")
print(f"✓ Medicamentos: {len(medicamentos)}")
print(f"✓ Consultas Médicas: {len(consultas)}")
print(f"✓ Tratamientos: {len(tratamientos)}")
print(f"✓ Recetas Médicas: {len(recetas)}")
print("="*50)
print("¡Carga de datos completada exitosamente!")