from django.db import models

# Create your models here.

class SeguroSalud(models.Model):  # (Mejora: nueva tabla)
    nombre = models.CharField(max_length=100, unique=True)
    contacto = models.CharField(max_length=120, blank=True)
    def __str__(self): return self.nombre

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    def __str__(self): return self.nombre

class Paciente(models.Model):
    class Genero(models.TextChoices):  # (Mejora: CHOICES)
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        OTRO = "O", "Otro"
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    genero = models.CharField(max_length=1, choices=Genero.choices)
    fecha_nacimiento = models.DateField()
    seguro = models.ForeignKey(SeguroSalud, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return f"{self.nombres} {self.apellidos} ({self.rut})"

class Medico(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    def __str__(self): return f"Dr(a). {self.apellidos}, {self.nombres}"

class Medicamento(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    def __str__(self): return self.nombre

class Tratamiento(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    medicamentos = models.ManyToManyField(Medicamento, blank=True)
    def __str__(self): return self.nombre

class ConsultaMedica(models.Model):
    class Estado(models.TextChoices):  # (Mejora: CHOICES estado de cita)
        AGENDADA = "AG", "Agendada"
        ATENDIDA = "AT", "Atendida"
        CANCELADA = "CA", "Cancelada"
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=2, choices=Estado.choices, default=Estado.AGENDADA)
    def __str__(self): return f"{self.fecha:%Y-%m-%d %H:%M} - {self.paciente} / {self.medico}"

class RecetaMedica(models.Model):
    consulta = models.OneToOneField(ConsultaMedica, on_delete=models.CASCADE)
    indicaciones = models.TextField()
    medicamentos = models.ManyToManyField(Medicamento, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Receta #{self.pk} - {self.consulta}"