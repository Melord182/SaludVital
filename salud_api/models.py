from django.db import models
#Importamos el modelo de usuario de Django
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.Choices('admin', 'Admin'), ('medico', 'Médico'), ('recepcionista', 'Recepcionista')
    def __str__(self):
        return self.user.username

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre
class Tipo_Sangre(models.Model):
    tipo = models.Choices('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    observacion = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.tipo

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo_sangre = models.ForeignKey(Tipo_Sangre, on_delete=models.SET_NULL, null=True)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    
class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    def __str__(self):
        return self.nombre

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    stock = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nombre

class Consulta_Medica(models.Model):
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_id = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField()
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')
    def __str__(self):
        return f"Consulta de {self.paciente_id} con {self.medico_id} el {self.fecha_consulta}"
    
class Tratamiento(models.Model):
    consulta_id = models.ForeignKey(Consulta_Medica, on_delete=models.CASCADE)
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Tratamiento para {self.consulta_id}"
    
class Receta_Medica(models.Model):
    tratamiento_id = models.ForeignKey(Tratamiento, on_delete=models.CASCADE)
    medicamento_id = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=100)    
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    def __str__(self):
        return f"Receta de {self.medicamento_id} para {self.tratamiento_id}"