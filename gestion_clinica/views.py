"""
Vistas para la API REST y vistas basadas en templates del sistema de gestión de clínica.
Implementa ViewSets para la API y vistas de templates para CRUD.
"""

from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica
)
from .serializers import (
    EspecialidadSerializer, PacienteSerializer, MedicoSerializer,
    ConsultaMedicaSerializer, TratamientoSerializer,
    MedicamentoSerializer, RecetaMedicaSerializer
)
from .filters import (
    EspecialidadFilter, PacienteFilter, MedicoFilter,
    ConsultaMedicaFilter, TratamientoFilter,
    MedicamentoFilter, RecetaMedicaFilter
)


# =============================================
# VIEWSETS PARA API REST
# =============================================

class EspecialidadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar especialidades médicas vía API.
    """
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filterset_class = EspecialidadFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']


class PacienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pacientes vía API.
    """
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filterset_class = PacienteFilter
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'rut']
    ordering_fields = ['apellido_paterno', 'fecha_registro']


class MedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar médicos vía API.
    Permite filtrar por especialidad.
    """
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filterset_class = MedicoFilter
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'especialidad__nombre']
    ordering_fields = ['apellido_paterno', 'especialidad__nombre']


class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar consultas médicas vía API.
    Permite filtrar por médico, paciente y especialidad.
    """
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaMedicaSerializer
    filterset_class = ConsultaMedicaFilter
    search_fields = ['paciente__nombre', 'medico__nombre', 'diagnostico']
    ordering_fields = ['fecha_hora', 'estado']


class TratamientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tratamientos vía API.
    """
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filterset_class = TratamientoFilter
    search_fields = ['descripcion', 'indicaciones']
    ordering_fields = ['fecha_inicio', 'fecha_fin']


class MedicamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar medicamentos vía API.
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filterset_class = MedicamentoFilter
    search_fields = ['nombre', 'principio_activo', 'laboratorio']
    ordering_fields = ['nombre', 'laboratorio']


class RecetaMedicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar recetas médicas vía API.
    """
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    filterset_class = RecetaMedicaFilter
    search_fields = ['medicamento__nombre', 'dosis']
    ordering_fields = ['fecha_emision']


# =============================================
# VISTAS BASADAS EN TEMPLATES - HOME
# =============================================

def home(request):
    """
    Vista principal del sistema.
    """
    context = {
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_medicos': Medico.objects.filter(activo=True).count(),
        'total_especialidades': Especialidad.objects.filter(activa=True).count(),
        'total_consultas': ConsultaMedica.objects.count(),
    }
    return render(request, 'home.html', context)


# =============================================
# VISTAS BASADAS EN TEMPLATES - ESPECIALIDAD
# =============================================

def especialidad_lista(request):
    """
    Lista todas las especialidades.
    """
    especialidades = Especialidad.objects.all()
    return render(request, 'especialidad/lista.html', {'especialidades': especialidades})


def especialidad_crear(request):
    """
    Crea una nueva especialidad.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        activa = request.POST.get('activa') == 'on'
        
        Especialidad.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            activa=activa
        )
        messages.success(request, 'Especialidad creada exitosamente.')
        return redirect('especialidad_lista')
    
    return render(request, 'especialidad/crear.html')


def especialidad_editar(request, pk):
    """
    Edita una especialidad existente.
    """
    especialidad = get_object_or_404(Especialidad, pk=pk)
    
    if request.method == 'POST':
        especialidad.nombre = request.POST.get('nombre')
        especialidad.descripcion = request.POST.get('descripcion', '')
        especialidad.activa = request.POST.get('activa') == 'on'
        especialidad.save()
        
        messages.success(request, 'Especialidad actualizada exitosamente.')
        return redirect('especialidad_lista')
    
    return render(request, 'especialidad/editar.html', {'especialidad': especialidad})


def especialidad_eliminar(request, pk):
    """
    Elimina una especialidad.
    """
    especialidad = get_object_or_404(Especialidad, pk=pk)
    
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, 'Especialidad eliminada exitosamente.')
        return redirect('especialidad_lista')
    
    return render(request, 'especialidad/eliminar.html', {'especialidad': especialidad})


# =============================================
# VISTAS BASADAS EN TEMPLATES - PACIENTE
# =============================================

def paciente_lista(request):
    """
    Lista todos los pacientes.
    """
    pacientes = Paciente.objects.all()
    return render(request, 'paciente/lista.html', {'pacientes': pacientes})


def paciente_crear(request):
    """
    Crea un nuevo paciente.
    """
    if request.method == 'POST':
        Paciente.objects.create(
            rut=request.POST.get('rut'),
            nombre=request.POST.get('nombre'),
            apellido_paterno=request.POST.get('apellido_paterno'),
            apellido_materno=request.POST.get('apellido_materno'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email', ''),
            direccion=request.POST.get('direccion'),
            prevision=request.POST.get('prevision'),
            activo=request.POST.get('activo') == 'on'
        )
        messages.success(request, 'Paciente creado exitosamente.')
        return redirect('paciente_lista')
    
    previsiones = Paciente.PREVISION_CHOICES
    return render(request, 'paciente/crear.html', {'previsiones': previsiones})


def paciente_editar(request, pk):
    """
    Edita un paciente existente.
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        paciente.rut = request.POST.get('rut')
        paciente.nombre = request.POST.get('nombre')
        paciente.apellido_paterno = request.POST.get('apellido_paterno')
        paciente.apellido_materno = request.POST.get('apellido_materno')
        paciente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        paciente.telefono = request.POST.get('telefono')
        paciente.email = request.POST.get('email', '')
        paciente.direccion = request.POST.get('direccion')
        paciente.prevision = request.POST.get('prevision')
        paciente.activo = request.POST.get('activo') == 'on'
        paciente.save()
        
        messages.success(request, 'Paciente actualizado exitosamente.')
        return redirect('paciente_lista')
    
    previsiones = Paciente.PREVISION_CHOICES
    return render(request, 'paciente/editar.html', {'paciente': paciente, 'previsiones': previsiones})


def paciente_eliminar(request, pk):
    """
    Elimina un paciente.
    """
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado exitosamente.')
        return redirect('paciente_lista')
    
    return render(request, 'paciente/eliminar.html', {'paciente': paciente})


# =============================================
# VISTAS BASADAS EN TEMPLATES - MEDICO
# =============================================

def medico_lista(request):
    """
    Lista todos los médicos.
    """
    medicos = Medico.objects.all()
    return render(request, 'medico/lista.html', {'medicos': medicos})


def medico_crear(request):
    """
    Crea un nuevo médico.
    """
    if request.method == 'POST':
        Medico.objects.create(
            rut=request.POST.get('rut'),
            nombre=request.POST.get('nombre'),
            apellido_paterno=request.POST.get('apellido_paterno'),
            apellido_materno=request.POST.get('apellido_materno'),
            especialidad_id=request.POST.get('especialidad'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            numero_registro=request.POST.get('numero_registro'),
            jornada=request.POST.get('jornada'),
            fecha_ingreso=request.POST.get('fecha_ingreso'),
            activo=request.POST.get('activo') == 'on'
        )
        messages.success(request, 'Médico creado exitosamente.')
        return redirect('medico_lista')
    
    especialidades = Especialidad.objects.filter(activa=True)
    jornadas = Medico.JORNADA_CHOICES
    return render(request, 'medico/crear.html', {'especialidades': especialidades, 'jornadas': jornadas})


def medico_editar(request, pk):
    """
    Edita un médico existente.
    """
    medico = get_object_or_404(Medico, pk=pk)
    
    if request.method == 'POST':
        medico.rut = request.POST.get('rut')
        medico.nombre = request.POST.get('nombre')
        medico.apellido_paterno = request.POST.get('apellido_paterno')
        medico.apellido_materno = request.POST.get('apellido_materno')
        medico.especialidad_id = request.POST.get('especialidad')
        medico.telefono = request.POST.get('telefono')
        medico.email = request.POST.get('email')
        medico.numero_registro = request.POST.get('numero_registro')
        medico.jornada = request.POST.get('jornada')
        medico.fecha_ingreso = request.POST.get('fecha_ingreso')
        medico.activo = request.POST.get('activo') == 'on'
        medico.save()
        
        messages.success(request, 'Médico actualizado exitosamente.')
        return redirect('medico_lista')
    
    especialidades = Especialidad.objects.filter(activa=True)
    jornadas = Medico.JORNADA_CHOICES
    return render(request, 'medico/editar.html', {'medico': medico, 'especialidades': especialidades, 'jornadas': jornadas})


def medico_eliminar(request, pk):
    """
    Elimina un médico.
    """
    medico = get_object_or_404(Medico, pk=pk)
    
    if request.method == 'POST':
        medico.delete()
        messages.success(request, 'Médico eliminado exitosamente.')
        return redirect('medico_lista')
    
    return render(request, 'medico/eliminar.html', {'medico': medico})

"""
Continuación de vistas para CRUD de Consulta Médica, Tratamiento, Medicamento y Receta Médica.
Agregar este código al archivo views.py
"""

# =============================================
# VISTAS BASADAS EN TEMPLATES - CONSULTA MÉDICA
# =============================================

def consulta_lista(request):
    """
    Lista todas las consultas médicas.
    """
    consultas = ConsultaMedica.objects.all()
    return render(request, 'consulta/lista.html', {'consultas': consultas})


def consulta_crear(request):
    """
    Crea una nueva consulta médica.
    """
    if request.method == 'POST':
        ConsultaMedica.objects.create(
            paciente_id=request.POST.get('paciente'),
            medico_id=request.POST.get('medico'),
            fecha_hora=request.POST.get('fecha_hora'),
            motivo_consulta=request.POST.get('motivo_consulta'),
            diagnostico=request.POST.get('diagnostico', ''),
            observaciones=request.POST.get('observaciones', ''),
            estado=request.POST.get('estado')
        )
        messages.success(request, 'Consulta médica creada exitosamente.')
        return redirect('consulta_lista')
    
    pacientes = Paciente.objects.filter(activo=True)
    medicos = Medico.objects.filter(activo=True)
    estados = ConsultaMedica.ESTADO_CHOICES
    return render(request, 'consulta/crear.html', {
        'pacientes': pacientes,
        'medicos': medicos,
        'estados': estados
    })


def consulta_editar(request, pk):
    """
    Edita una consulta médica existente.
    """
    consulta = get_object_or_404(ConsultaMedica, pk=pk)
    
    if request.method == 'POST':
        consulta.paciente_id = request.POST.get('paciente')
        consulta.medico_id = request.POST.get('medico')
        consulta.fecha_hora = request.POST.get('fecha_hora')
        consulta.motivo_consulta = request.POST.get('motivo_consulta')
        consulta.diagnostico = request.POST.get('diagnostico', '')
        consulta.observaciones = request.POST.get('observaciones', '')
        consulta.estado = request.POST.get('estado')
        consulta.save()
        
        messages.success(request, 'Consulta médica actualizada exitosamente.')
        return redirect('consulta_lista')
    
    pacientes = Paciente.objects.filter(activo=True)
    medicos = Medico.objects.filter(activo=True)
    estados = ConsultaMedica.ESTADO_CHOICES
    return render(request, 'consulta/editar.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos,
        'estados': estados
    })


def consulta_eliminar(request, pk):
    """
    Elimina una consulta médica.
    """
    consulta = get_object_or_404(ConsultaMedica, pk=pk)
    
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta médica eliminada exitosamente.')
        return redirect('consulta_lista')
    
    return render(request, 'consulta/eliminar.html', {'consulta': consulta})


# =============================================
# VISTAS BASADAS EN TEMPLATES - TRATAMIENTO
# =============================================

def tratamiento_lista(request):
    """
    Lista todos los tratamientos.
    """
    tratamientos = Tratamiento.objects.all()
    return render(request, 'tratamiento/lista.html', {'tratamientos': tratamientos})


def tratamiento_crear(request):
    """
    Crea un nuevo tratamiento.
    """
    if request.method == 'POST':
        Tratamiento.objects.create(
            consulta_id=request.POST.get('consulta'),
            descripcion=request.POST.get('descripcion'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            indicaciones=request.POST.get('indicaciones'),
            activo=request.POST.get('activo') == 'on'
        )
        messages.success(request, 'Tratamiento creado exitosamente.')
        return redirect('tratamiento_lista')
    
    consultas = ConsultaMedica.objects.filter(estado='REALIZADA')
    return render(request, 'tratamiento/crear.html', {'consultas': consultas})


def tratamiento_editar(request, pk):
    """
    Edita un tratamiento existente.
    """
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if request.method == 'POST':
        tratamiento.consulta_id = request.POST.get('consulta')
        tratamiento.descripcion = request.POST.get('descripcion')
        tratamiento.fecha_inicio = request.POST.get('fecha_inicio')
        tratamiento.fecha_fin = request.POST.get('fecha_fin') or None
        tratamiento.indicaciones = request.POST.get('indicaciones')
        tratamiento.activo = request.POST.get('activo') == 'on'
        tratamiento.save()
        
        messages.success(request, 'Tratamiento actualizado exitosamente.')
        return redirect('tratamiento_lista')
    
    consultas = ConsultaMedica.objects.filter(estado='REALIZADA')
    return render(request, 'tratamiento/editar.html', {
        'tratamiento': tratamiento,
        'consultas': consultas
    })


def tratamiento_eliminar(request, pk):
    """
    Elimina un tratamiento.
    """
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if request.method == 'POST':
        tratamiento.delete()
        messages.success(request, 'Tratamiento eliminado exitosamente.')
        return redirect('tratamiento_lista')
    
    return render(request, 'tratamiento/eliminar.html', {'tratamiento': tratamiento})


# =============================================
# VISTAS BASADAS EN TEMPLATES - MEDICAMENTO
# =============================================

def medicamento_lista(request):
    """
    Lista todos los medicamentos.
    """
    medicamentos = Medicamento.objects.all()
    return render(request, 'medicamento/lista.html', {'medicamentos': medicamentos})


def medicamento_crear(request):
    """
    Crea un nuevo medicamento.
    """
    if request.method == 'POST':
        Medicamento.objects.create(
            nombre=request.POST.get('nombre'),
            principio_activo=request.POST.get('principio_activo'),
            presentacion=request.POST.get('presentacion'),
            concentracion=request.POST.get('concentracion'),
            laboratorio=request.POST.get('laboratorio'),
            requiere_receta=request.POST.get('requiere_receta') == 'on',
            stock_disponible=request.POST.get('stock_disponible', 0),
            activo=request.POST.get('activo') == 'on'
        )
        messages.success(request, 'Medicamento creado exitosamente.')
        return redirect('medicamento_lista')
    
    return render(request, 'medicamento/crear.html')


def medicamento_editar(request, pk):
    """
    Edita un medicamento existente.
    """
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.nombre = request.POST.get('nombre')
        medicamento.principio_activo = request.POST.get('principio_activo')
        medicamento.presentacion = request.POST.get('presentacion')
        medicamento.concentracion = request.POST.get('concentracion')
        medicamento.laboratorio = request.POST.get('laboratorio')
        medicamento.requiere_receta = request.POST.get('requiere_receta') == 'on'
        medicamento.stock_disponible = request.POST.get('stock_disponible', 0)
        medicamento.activo = request.POST.get('activo') == 'on'
        medicamento.save()
        
        messages.success(request, 'Medicamento actualizado exitosamente.')
        return redirect('medicamento_lista')
    
    return render(request, 'medicamento/editar.html', {'medicamento': medicamento})


def medicamento_eliminar(request, pk):
    """
    Elimina un medicamento.
    """
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, 'Medicamento eliminado exitosamente.')
        return redirect('medicamento_lista')
    
    return render(request, 'medicamento/eliminar.html', {'medicamento': medicamento})


# =============================================
# VISTAS BASADAS EN TEMPLATES - RECETA MÉDICA
# =============================================

def receta_lista(request):
    """
    Lista todas las recetas médicas.
    """
    recetas = RecetaMedica.objects.all()
    return render(request, 'receta/lista.html', {'recetas': recetas})


def receta_crear(request):
    """
    Crea una nueva receta médica.
    """
    if request.method == 'POST':
        RecetaMedica.objects.create(
            tratamiento_id=request.POST.get('tratamiento'),
            medicamento_id=request.POST.get('medicamento'),
            dosis=request.POST.get('dosis'),
            frecuencia=request.POST.get('frecuencia'),
            duracion=request.POST.get('duracion'),
            cantidad_total=request.POST.get('cantidad_total'),
            instrucciones_especiales=request.POST.get('instrucciones_especiales', '')
        )
        messages.success(request, 'Receta médica creada exitosamente.')
        return redirect('receta_lista')
    
    tratamientos = Tratamiento.objects.filter(activo=True)
    medicamentos = Medicamento.objects.filter(activo=True)
    return render(request, 'receta/crear.html', {
        'tratamientos': tratamientos,
        'medicamentos': medicamentos
    })


def receta_editar(request, pk):
    """
    Edita una receta médica existente.
    """
    receta = get_object_or_404(RecetaMedica, pk=pk)
    
    if request.method == 'POST':
        receta.tratamiento_id = request.POST.get('tratamiento')
        receta.medicamento_id = request.POST.get('medicamento')
        receta.dosis = request.POST.get('dosis')
        receta.frecuencia = request.POST.get('frecuencia')
        receta.duracion = request.POST.get('duracion')
        receta.cantidad_total = request.POST.get('cantidad_total')
        receta.instrucciones_especiales = request.POST.get('instrucciones_especiales', '')
        receta.save()
        
        messages.success(request, 'Receta médica actualizada exitosamente.')
        return redirect('receta_lista')
    
    tratamientos = Tratamiento.objects.filter(activo=True)
    medicamentos = Medicamento.objects.filter(activo=True)
    return render(request, 'receta/editar.html', {
        'receta': receta,
        'tratamientos': tratamientos,
        'medicamentos': medicamentos
    })


def receta_eliminar(request, pk):
    """
    Elimina una receta médica.
    """
    receta = get_object_or_404(RecetaMedica, pk=pk)
    
    if request.method == 'POST':
        receta.delete()
        messages.success(request, 'Receta médica eliminada exitosamente.')
        return redirect('receta_lista')
    
    return render(request, 'receta/eliminar.html', {'receta': receta})