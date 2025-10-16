# -*- coding: utf-8 -*-
"""
Archivo: datos_iniciales.py

Descripción
-----------
Script para poblar la base de datos con datos realistas del sistema de gestión clínica,
**incluyendo Laboratorios** y asignando `Medicamento.laboratorio` como ForeignKey correctamente.

Cómo ejecutarlo
---------------
- Windows PowerShell:
    Get-Content .\datos_iniciales.py | python manage.py shell
- CMD / Bash:
    python manage.py shell < datos_iniciales.py
- Interactivo:
    python manage.py shell
    >>> exec(open('datos_iniciales.py', encoding='utf-8').read())

Advertencia
-----------
El script **elimina** datos existentes (modo desarrollo). Úsalo con cuidado.
"""

from datetime import date, datetime, timedelta
import random

from gestion_clinica.models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica, Laboratorio
)

print('Iniciando carga de datos...')

# -------------------------------------------------
# 0) LIMPIEZA (orden seguro por dependencias)
# -------------------------------------------------
# Receta -> Tratamiento -> Consulta -> Medicamento -> Laboratorio -> Medico -> Paciente -> Especialidad
RecetaMedica.objects.all().delete()
Tratamiento.objects.all().delete()
ConsultaMedica.objects.all().delete()
Medicamento.objects.all().delete()
Laboratorio.objects.all().delete()
Medico.objects.all().delete()
Paciente.objects.all().delete()
Especialidad.objects.all().delete()

print('Datos anteriores eliminados.')

# -------------------------------------------------
# 1) ESPECIALIDADES
# -------------------------------------------------
especialidades_data = [
    {'nombre': 'Cardiología', 'descripcion': 'Enfermedades del corazón y sistema circulatorio'},
    {'nombre': 'Pediatría', 'descripcion': 'Atención de niños y adolescentes'},
    {'nombre': 'Traumatología', 'descripcion': 'Sistema musculoesquelético'},
    {'nombre': 'Medicina General', 'descripcion': 'Atención integral y preventiva'},
    {'nombre': 'Ginecología', 'descripcion': 'Salud femenina'},
    {'nombre': 'Dermatología', 'descripcion': 'Enfermedades de la piel'},
    {'nombre': 'Oftalmología', 'descripcion': 'Salud visual'},
]

especialidades = [
    Especialidad.objects.create(**esp, activa=True)
    for esp in especialidades_data
]
for e in especialidades:
    print(f'✓ Especialidad creada: {e.nombre}')

# -------------------------------------------------
# 2) PACIENTES
# -------------------------------------------------
pacientes_data = [
    {'rut': '12345678-9', 'nombre': 'María', 'apellido_paterno': 'González', 'apellido_materno': 'López',
     'fecha_nacimiento': date(1985, 3, 15), 'telefono': '+56912345678', 'email': 'maria.gonzalez@email.com',
     'direccion': 'Av. Libertador 1234, Santiago', 'prevision': 'FONASA'},
    {'rut': '23456789-0', 'nombre': 'Juan', 'apellido_paterno': 'Pérez', 'apellido_materno': 'Soto',
     'fecha_nacimiento': date(1990, 7, 22), 'telefono': '+56923456789', 'email': 'juan.perez@email.com',
     'direccion': 'Calle Principal 567, Providencia', 'prevision': 'ISAPRE'},
    {'rut': '34567890-1', 'nombre': 'Ana', 'apellido_paterno': 'Martínez', 'apellido_materno': 'Rojas',
     'fecha_nacimiento': date(1978, 11, 8), 'telefono': '+56934567890', 'email': 'ana.martinez@email.com',
     'direccion': 'Pasaje Los Robles 890, Las Condes', 'prevision': 'FONASA'},
    {'rut': '45678901-2', 'nombre': 'Carlos', 'apellido_paterno': 'Silva', 'apellido_materno': 'Vargas',
     'fecha_nacimiento': date(1995, 5, 30), 'telefono': '+56945678901', 'email': 'carlos.silva@email.com',
     'direccion': 'Av. Apoquindo 2345, Las Condes', 'prevision': 'PARTICULAR'},
    {'rut': '56789012-3', 'nombre': 'Patricia', 'apellido_paterno': 'Fernández', 'apellido_materno': 'Muñoz',
     'fecha_nacimiento': date(1982, 9, 12), 'telefono': '+56956789012', 'email': 'patricia.fernandez@email.com',
     'direccion': 'Calle Los Pinos 456, Ñuñoa', 'prevision': 'ISAPRE'},
]

pacientes = [Paciente.objects.create(**p, activo=True) for p in pacientes_data]
for p in pacientes:
    print(f'✓ Paciente creado: {p.nombre_completo}')

# -------------------------------------------------
# 3) MÉDICOS
# -------------------------------------------------
medicos_data = [
    {'rut': '11111111-1', 'nombre': 'Roberto', 'apellido_paterno': 'Carrasco', 'apellido_materno': 'Torres',
     'telefono': '+56911111111', 'email': 'r.carrasco@clinica.cl', 'numero_registro': 'REG-001',
     'fecha_ingreso': date(2015, 1, 10), 'jornada': 'COMPLETA'},
    {'rut': '22222222-2', 'nombre': 'Laura', 'apellido_paterno': 'Ramírez', 'apellido_materno': 'Núñez',
     'telefono': '+56922222222', 'email': 'l.ramirez@clinica.cl', 'numero_registro': 'REG-002',
     'fecha_ingreso': date(2018, 5, 20), 'jornada': 'COMPLETA'},
    {'rut': '33333333-3', 'nombre': 'Diego', 'apellido_paterno': 'Morales', 'apellido_materno': 'Castro',
     'telefono': '+56933333333', 'email': 'd.morales@clinica.cl', 'numero_registro': 'REG-003',
     'fecha_ingreso': date(2020, 3, 15), 'jornada': 'PARCIAL'},
    {'rut': '44444444-4', 'nombre': 'Carmen', 'apellido_paterno': 'Vega', 'apellido_materno': 'Bravo',
     'telefono': '+56944444444', 'email': 'c.vega@clinica.cl', 'numero_registro': 'REG-004',
     'fecha_ingreso': date(2017, 9, 1), 'jornada': 'COMPLETA'},
]

medicos = []
for i, m in enumerate(medicos_data):
    esp = especialidades[i % len(especialidades)]
    medico = Medico.objects.create(**m, especialidad=esp, activo=True)
    medicos.append(medico)
    print(f'✓ Médico creado: {medico.nombre_completo} - {esp.nombre}')

# -------------------------------------------------
# 4) LABORATORIOS (NUEVO)
# -------------------------------------------------
laboratorios_data = [
    {'nombre': 'Laboratorio Chile', 'pais': 'Chile', 'direccion': 'Av. Independencia 1000, Santiago', 'telefono': '+56222222222', 'email': 'contacto@labchile.cl'},
    {'nombre': 'Farma Plus', 'pais': 'Chile', 'direccion': 'Av. Providencia 123, Santiago', 'telefono': '+56223334444', 'email': 'info@farmaplus.cl'},
    {'nombre': 'Antibióticos S.A.', 'pais': 'Chile', 'direccion': 'Camino Industrial 456, Quilicura', 'telefono': '+56225556666', 'email': 'ventas@antibioticossa.cl'},
    {'nombre': 'CardioMed', 'pais': 'Chile', 'direccion': 'Av. Las Condes 7890, Las Condes', 'telefono': '+56227778888', 'email': 'support@cardiomed.cl'},
    {'nombre': 'Gastro Lab', 'pais': 'Chile', 'direccion': 'Av. Italia 234, Providencia', 'telefono': '+56229990000', 'email': 'contacto@gastrolab.cl'},
    {'nombre': 'Genéricos Andinos', 'pais': 'Perú', 'direccion': 'Av. Arequipa 1234, Lima', 'telefono': '+5111234567', 'email': 'hola@genericosandinos.pe'},
]

laboratorios = {}
for lab in laboratorios_data:
    obj, _ = Laboratorio.objects.get_or_create(nombre=lab['nombre'], defaults={
        'pais': lab.get('pais', 'Chile'),
        'direccion': lab.get('direccion', ''),
        'telefono': lab.get('telefono', ''),
        'email': lab.get('email', ''),
        'activo': True,
    })
    laboratorios[obj.nombre] = obj
    print(f'✓ Laboratorio cargado: {obj.nombre} ({obj.pais})')

# -------------------------------------------------
# 5) MEDICAMENTOS (usando FK a Laboratorio)
# -------------------------------------------------
medicamentos_data = [
    {'nombre': 'Paracetamol', 'principio_activo': 'Paracetamol', 'presentacion': 'Tabletas',
     'concentracion': '500mg', 'laboratorio_nombre': 'Laboratorio Chile', 'requiere_receta': False, 'stock_disponible': 500},
    {'nombre': 'Ibuprofeno', 'principio_activo': 'Ibuprofeno', 'presentacion': 'Cápsulas',
     'concentracion': '400mg', 'laboratorio_nombre': 'Farma Plus', 'requiere_receta': False, 'stock_disponible': 300},
    {'nombre': 'Amoxicilina', 'principio_activo': 'Amoxicilina', 'presentacion': 'Cápsulas',
     'concentracion': '500mg', 'laboratorio_nombre': 'Antibióticos S.A.', 'requiere_receta': True, 'stock_disponible': 200},
    {'nombre': 'Losartán', 'principio_activo': 'Losartán', 'presentacion': 'Tabletas',
     'concentracion': '50mg', 'laboratorio_nombre': 'CardioMed', 'requiere_receta': True, 'stock_disponible': 150},
    {'nombre': 'Omeprazol', 'principio_activo': 'Omeprazol', 'presentacion': 'Cápsulas',
     'concentracion': '20mg', 'laboratorio_nombre': 'Gastro Lab', 'requiere_receta': False, 'stock_disponible': 250},
]

medicamentos = []
for md in medicamentos_data:
    lab = laboratorios.get(md['laboratorio_nombre'])
    if lab is None:
        # en caso de que el laboratorio no exista por alguna razón, créalo al vuelo
        lab, _ = Laboratorio.objects.get_or_create(nombre=md['laboratorio_nombre'], defaults={'pais': 'Chile', 'activo': True})
        laboratorios[lab.nombre] = lab
    obj = Medicamento.objects.create(
        nombre=md['nombre'],
        principio_activo=md['principio_activo'],
        presentacion=md['presentacion'],
        concentracion=md['concentracion'],
        laboratorio=lab,
        requiere_receta=md['requiere_receta'],
        stock_disponible=md['stock_disponible'],
        activo=True
    )
    medicamentos.append(obj)
    print(f'✓ Medicamento creado: {obj.nombre} ({lab.nombre})')

# -------------------------------------------------
# 6) CONSULTAS
# -------------------------------------------------
consultas = []
estados = ['AGENDADA', 'REALIZADA', 'CANCELADA', 'NO_ASISTIO']
motivos = [
    'Dolor abdominal persistente',
    'Control de presión arterial',
    'Dolor de cabeza frecuente',
    'Control pediátrico rutinario',
    'Dolor en articulaciones',
    'Chequeo general de salud',
    'Problemas respiratorios',
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
        diagnostico='Diagnóstico médico según evaluación clínica.' if estado == 'REALIZADA' else '',
        observaciones='Paciente estable, seguir indicaciones.' if estado == 'REALIZADA' else '',
        estado=estado
    )
    consultas.append(consulta)
    print(f'✓ Consulta creada: {consulta.id} - {paciente.nombre} con Dr(a). {medico.apellido_paterno}')

# -------------------------------------------------
# 7) TRATAMIENTOS para consultas REALIZADAS
# -------------------------------------------------
tratamientos = []
consultas_realizadas = [c for c in consultas if c.estado == 'REALIZADA']

for consulta in consultas_realizadas[:5]:
    fecha_inicio = consulta.fecha_hora.date()
    fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 30))

    tratamiento = Tratamiento.objects.create(
        consulta=consulta,
        descripcion=f'Tratamiento para {consulta.motivo_consulta.lower()}',
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        indicaciones='Reposo relativo. Tomar medicación según indicaciones. Control en 15 días.',
        activo=True
    )
    tratamientos.append(tratamiento)
    print(f'✓ Tratamiento creado: {tratamiento.id} - Consulta {consulta.id}')

# -------------------------------------------------
# 8) RECETAS (1 a 3 por tratamiento)
# -------------------------------------------------
recetas = []
dosis_opciones = ['1 tableta', '2 tabletas', '1 cápsula', '2 cápsulas']
frecuencia_opciones = ['Cada 8 horas', 'Cada 12 horas', 'Una vez al día', 'Dos veces al día']
duracion_opciones = ['7 días', '10 días', '14 días', '30 días']

for t in tratamientos:
    for medicamento in random.sample(medicamentos, random.randint(1, 3)):
        receta = RecetaMedica.objects.create(
            tratamiento=t,
            medicamento=medicamento,
            dosis=random.choice(dosis_opciones),
            frecuencia=random.choice(frecuencia_opciones),
            duracion=random.choice(duracion_opciones),
            cantidad_total=random.randint(10, 60),
            instrucciones_especiales='Tomar con alimentos. Evitar alcohol durante el tratamiento.'
        )
        recetas.append(receta)
        print(f'✓ Receta creada: {receta.id} - {medicamento.nombre}')

# -------------------------------------------------
# 9) RESUMEN
# -------------------------------------------------
print('\n' + '='*50)
print('RESUMEN DE DATOS CARGADOS')
print('='*50)
print(f'✓ Especialidades: {len(especialidades)}')
print(f'✓ Pacientes: {len(pacientes)}')
print(f'✓ Médicos: {len(medicos)}')
print(f'✓ Laboratorios: {len(laboratorios)}')
print(f'✓ Medicamentos: {len(medicamentos)}')
print(f'✓ Consultas Médicas: {len(consultas)}')
print(f'✓ Tratamientos: {len(tratamientos)}')
print(f'✓ Recetas Médicas: {len(recetas)}')
print('='*50)
print('¡Carga de datos completada exitosamente!')
