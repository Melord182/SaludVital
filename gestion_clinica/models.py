"""
Archivo: models.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este archivo define los **modelos de datos (ORM)** utilizados en el sistema de gestión clínica **Salud Vital Ltda.**.  
Cada clase representa una **entidad del dominio médico-administrativo**, que se almacena como una tabla en la base de datos.

Los modelos están diseñados para cubrir todos los aspectos esenciales de una clínica:
- **Especialidades** médicas disponibles.
- **Pacientes** registrados con sus datos personales y previsión de salud.
- **Médicos** asociados a una especialidad.
- **Consultas médicas** entre pacientes y médicos.
- **Medicamentos** administrados por la clínica.
- **Tratamientos** derivados de una consulta.
- **Recetas médicas** vinculadas a tratamientos y medicamentos.

La estructura sigue las buenas prácticas del ORM de Django:
- Relaciones **ForeignKey** para conectar entidades relacionadas.
- Uso de **choices**, **validadores** y **propiedades personalizadas**.
- Configuración de **Meta** para definir nombres legibles y ordenamientos por defecto.

OBJETIVOS DEL MODELO:
---------------------
✔ Modelar de forma coherente y escalable los procesos clínicos.  
✔ Facilitar consultas complejas mediante relaciones ORM.  
✔ Integrarse fácilmente con Django Admin y Django REST Framework.  
✔ Mantener integridad referencial mediante claves foráneas y restricciones.  

RELACIONES ENTRE MODELOS:
-------------------------
- **Medico** ➜ pertenece a una **Especialidad**.  
- **ConsultaMedica** ➜ une un **Paciente** con un **Medico**.  
- **Tratamiento** ➜ está asociado a una **ConsultaMedica**.  
- **RecetaMedica** ➜ relaciona un **Tratamiento** con un **Medicamento**.  

FLUJO DE DATOS (EJEMPLO):
-------------------------
1️⃣ Un paciente agenda una consulta con un médico.  
2️⃣ Se genera una instancia de `ConsultaMedica`.  
3️⃣ El médico prescribe un `Tratamiento`.  
4️⃣ De ese tratamiento se derivan una o más `RecetaMedica`.  
5️⃣ Cada receta referencia a un `Medicamento` existente en el stock.

DEPENDENCIAS:
-------------
- `django.db.models`: Base de la definición de modelos.  
- `django.core.validators`: Validadores numéricos y de rango.  

CONCLUSIÓN:
-----------
Este módulo constituye el **núcleo del sistema**, proporcionando la base estructural sobre la que se construyen las vistas, 
serializadores, formularios y API REST del proyecto.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Especialidad(models.Model):
    """
    Modelo para representar las especialidades médicas disponibles en la clínica.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    """
    Modelo para representar a los pacientes de la clínica.
    Incluye CHOICE para tipo de previsión.
    """
    # CHOICE para tipo de previsión (Mejora 1)
    PREVISION_CHOICES = [
        ('FONASA', 'FONASA'),
        ('ISAPRE', 'ISAPRE'),
        ('PARTICULAR', 'Particular'),
        ('OTRO', 'Otro'),
    ]
    
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200)
    prevision = models.CharField(max_length=20, choices=PREVISION_CHOICES, default='FONASA')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} - {self.rut}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"


class Medico(models.Model):
    """
    Modelo para representar a los médicos de la clínica.
    Incluye CHOICE para tipo de jornada.
    """
    # CHOICE para tipo de jornada (Mejora 2)
    JORNADA_CHOICES = [
        ('COMPLETA', 'Jornada Completa'),
        ('PARCIAL', 'Jornada Parcial'),
        ('TURNO', 'Por Turno'),
    ]
    
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='medicos')
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    numero_registro = models.CharField(max_length=20, unique=True)
    jornada = models.CharField(max_length=20, choices=JORNADA_CHOICES, default='COMPLETA')
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField()
    
    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
    
    def __str__(self):
        return f"Dr(a). {self.nombre} {self.apellido_paterno} - {self.especialidad.nombre}"
    
    @property
    def nombre_completo(self):
        return f"Dr(a). {self.nombre} {self.apellido_paterno} {self.apellido_materno}"


class ConsultaMedica(models.Model):
    """
    Modelo para representar las consultas médicas realizadas.
    Relaciona pacientes con médicos.
    """
    # CHOICE para estado de la consulta
    ESTADO_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
        ('NO_ASISTIO', 'No Asistió'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name='consultas')
    fecha_hora = models.DateTimeField()
    motivo_consulta = models.TextField()
    diagnostico = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='AGENDADA')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Consulta Médica'
        verbose_name_plural = 'Consultas Médicas'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"Consulta {self.id} - {self.paciente.nombre_completo} con {self.medico.nombre_completo}"


class Medicamento(models.Model):
    """
    Modelo para representar los medicamentos disponibles.
    """
    nombre = models.CharField(max_length=200)
    principio_activo = models.CharField(max_length=200)
    presentacion = models.CharField(max_length=100)
    concentracion = models.CharField(max_length=50)
    laboratorio = models.CharField(max_length=100)
    requiere_receta = models.BooleanField(default=True)
    stock_disponible = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.presentacion}"


class Tratamiento(models.Model):
    """
    Modelo para representar tratamientos médicos asociados a consultas.
    """
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE, related_name='tratamientos')
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    indicaciones = models.TextField()
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"Tratamiento {self.id} - Consulta {self.consulta.id}"


class RecetaMedica(models.Model):
    """
    Modelo para representar recetas médicas emitidas en consultas.
    Relaciona tratamientos con medicamentos.
    """
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='recetas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name='recetas')
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    cantidad_total = models.IntegerField(validators=[MinValueValidator(1)])
    instrucciones_especiales = models.TextField(blank=True)
    fecha_emision = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Receta Médica'
        verbose_name_plural = 'Recetas Médicas'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Receta {self.id} - {self.medicamento.nombre}"