from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta

from salud.models import (
    SeguroSalud,
    Especialidad,
    Medico,
    Paciente,
    Medicamento,
    Tratamiento,
    ConsultaMedica,
    RecetaMedica,
)

class Command(BaseCommand):
    help = "Carga datos de prueba para la app 'salud'"

    def handle(self, *args, **kwargs):
        fake = Faker("es_ES")

        # Seguros
        seguros = [
            SeguroSalud.objects.get_or_create(nombre=n)[0]
            for n in ["Fonasa", "Isapre Colmena", "Isapre Consalud"]
        ]
        # Especialidades
        cardio = Especialidad.objects.get_or_create(nombre="Cardiología")[0]
        derma = Especialidad.objects.get_or_create(nombre="Dermatología")[0]

        # Médicos
        medicos = []
        for _ in range(6):
            medicos.append(
                Medico.objects.get_or_create(
                    rut=fake.unique.msisdn()[:9],
                    nombres=fake.first_name(),
                    apellidos=fake.last_name(),
                    especialidad=choice([cardio, derma]),
                )[0]
            )

        # Pacientes
        pacientes = []
        for _ in range(20):
            pacientes.append(
                Paciente.objects.get_or_create(
                    rut=fake.unique.msisdn()[:9],
                    nombres=fake.first_name(),
                    apellidos=fake.last_name(),
                    genero=choice([Paciente.Genero.MASCULINO, Paciente.Genero.FEMENINO]),
                    fecha_nacimiento=fake.date_of_birth(minimum_age=1, maximum_age=90),
                    seguro=choice(seguros),
                )[0]
            )

        # Medicamentos / Tratamiento
        meds = [
            Medicamento.objects.get_or_create(nombre=n)[0]
            for n in ["Paracetamol", "Ibuprofeno", "Amoxicilina"]
        ]
        trat = Tratamiento.objects.get_or_create(
            nombre="Tratamiento estándar", descripcion="Indicaciones generales"
        )[0]
        trat.medicamentos.set(meds)

        # Consultas + Recetas
        for _ in range(40):
            c = ConsultaMedica.objects.create(
                paciente=choice(pacientes),
                medico=choice(medicos),
                fecha=datetime.now() - timedelta(days=randint(0, 60)),
                motivo="Control",
                estado=choice(list(ConsultaMedica.Estado.values)),
            )
            if choice([True, False]):
                r = RecetaMedica.objects.create(
                    consulta=c,
                    indicaciones="Tomar según indicación médica",
                )
                r.medicamentos.set([choice(meds)])

        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados."))
