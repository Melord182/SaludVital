"""
Archivo: views.py
Ubicación: Aplicación 'gestion_clinica'

DESCRIPCIÓN GENERAL:
--------------------
Este módulo reúne dos capas de presentación del sistema:
1) **API REST (ViewSets de DRF)** para consumo programático (frontend SPA, apps móviles, integraciones).
2) **Vistas basadas en templates (funciones)** para CRUD web tradicional con HTML.

CÓMO ESTÁ ORGANIZADO:
---------------------
- Sección "VIEWSETS PARA API REST":
  • Cada ViewSet hereda de `ModelViewSet` e incluye:
    - `queryset`: conjunto base de datos.
    - `serializer_class`: traducción a/desde JSON.
    - `filterset_class`: filtros declarativos con django-filter.
    - `search_fields`: búsqueda textual.
    - `ordering_fields`: campos permitidos para ordenamiento.
  • DRF generará rutas a través del `DefaultRouter` configurado en `urls.py`.

- Sección "VISTAS BASADAS EN TEMPLATES":
  • Vistas funcionales para `home` y CRUD de cada entidad.
  • Usan `render` para devolver HTML y `messages` para feedback al usuario.
  • `get_object_or_404` garantiza respuestas 404 seguras cuando un recurso no existe.
  • En acciones POST se redirige (PRG: Post/Redirect/Get) para evitar reenvíos.

BUENAS PRÁCTICAS APLICADAS:
---------------------------
- **Seguridad**: uso de `on_delete` apropiado en modelos (p. ej., `PROTECT` en claves clínicas sensibles).
- **UX**: mensajes de éxito con `django.contrib.messages`.
- **Mantenibilidad**: filtros centralizados en `filters.py` y serializadores en `serializers.py`.

EXTENSIONES SUGERIDAS (OPCIONAL):
---------------------------------
- **Paginación DRF**: configurar `DEFAULT_PAGINATION_CLASS` y `PAGE_SIZE` en settings.
- **Permisos DRF**: añadir `permission_classes` (p. ej., `IsAuthenticated`) y autenticación.
- **Formularios Django**: reemplazar acceso directo a `request.POST` por `ModelForm` para validación y limpieza.
"""

from django.db.models.deletion import ProtectedError
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
    Especialidad, Paciente, Medico, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica, Laboratorio
)
from .serializers import (
    EspecialidadSerializer, PacienteSerializer, MedicoSerializer,
    ConsultaMedicaSerializer, TratamientoSerializer,
    MedicamentoSerializer, RecetaMedicaSerializer, LaboratorioSerializer
)
from .filters import (
    EspecialidadFilter, PacienteFilter, MedicoFilter,
    ConsultaMedicaFilter, TratamientoFilter,
    MedicamentoFilter, RecetaMedicaFilter, LaboratorioFilter
)
from django.db.models import Count
from .forms import (
    EspecialidadForm, PacienteForm, MedicoForm,
    ConsultaMedicaForm, TratamientoForm,
    MedicamentoForm, RecetaMedicaForm, LaboratorioForm
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
    template_name = 'especialidad/lista.html'
    context_object_name = 'especialidades'
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']

class LaboratorioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar laboratorios vía API.
    """
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    filterset_class = LaboratorioFilter
    template_name = 'laboratorio/lista.html'
    context_object_name = 'laboratorios'
    search_fields = ['nombre', 'pais']
    ordering_fields = ['nombre', 'pais']

class PacienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pacientes vía API.
    """
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filterset_class = PacienteFilter
    template_name = 'paciente/lista.html'
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
    template_name = 'medico/lista.html'
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
    template_name = 'consulta/lista.html'
    search_fields = ['paciente__nombre', 'medico__nombre', 'diagnostico']
    ordering_fields = ['fecha_hora', 'estado']


class TratamientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tratamientos vía API.
    """
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filterset_class = TratamientoFilter
    template_name = 'tratamiento/lista.html'
    search_fields = ['descripcion', 'indicaciones']
    ordering_fields = ['fecha_inicio', 'fecha_fin']


class MedicamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar medicamentos vía API.
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filterset_class = MedicamentoFilter
    template_name = 'medicamento/lista.html'
    search_fields = ['nombre', 'principio_activo', 'laboratorio_nombre']
    ordering_fields = ['nombre', 'laboratorio_nombre']


class RecetaMedicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar recetas médicas vía API.
    """
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    filterset_class = RecetaMedicaFilter
    template_name = 'receta/lista.html'
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
    qs = Especialidad.objects.all()
    filtro = EspecialidadFilter(request.GET, queryset=Especialidad.objects.all())
    return render(request, 'especialidad/lista.html', {
        'filter': filtro,
        'especialidades': filtro.qs,
    })

def especialidad_crear(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad creada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm()
    return render(request, 'especialidad/crear.html', {'form': form})


def especialidad_editar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad actualizada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'especialidad/editar.html', {'form': form, 'especialidad': especialidad})


def especialidad_eliminar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)

    # Corta el flujo si está en uso (evita incluso mostrar el form)
    if especialidad.medicos.exists():
        messages.error(request, 'No se puede eliminar la especialidad: tiene médicos asociados. '
                                'Reasigna sus médicos o desactívala.')
        return redirect('especialidad_lista')

    if request.method == 'POST':
        try:
            especialidad.delete()
            messages.success(request, 'Especialidad eliminada exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar la especialidad: está en uso.')
        return redirect('especialidad_lista')

    return render(request, 'especialidad/eliminar.html', {'especialidad': especialidad})


# =============================================
# VISTAS BASADAS EN TEMPLATES - PACIENTE
# =============================================

def paciente_lista(request):
    qs = Paciente.objects.all()
    filtro = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    return render(request, 'paciente/lista.html', {
        'filter': filtro,
        'pacientes': filtro.qs,
    })
def paciente_crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm()
    return render(request, 'paciente/crear.html', {'form': form})


def laboratorio_lista(request):
    f = LaboratorioFilter(request.GET or None, queryset=Laboratorio.objects.all())
    return render(request, 'laboratorio/lista.html', {
        'filter': f,
        'laboratorios': f.qs,  # ¡usar el queryset filtrado!
    })

def laboratorio_crear(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratorio creado exitosamente.')
            return redirect('laboratorio_lista')
    else:
        form = LaboratorioForm()
    return render(request, 'laboratorio/crear.html', {'form': form})
def laboratorio_editar(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratorio actualizado exitosamente.')
            return redirect('laboratorio_lista')
    else:
        form = LaboratorioForm(instance=laboratorio)
    return render(request, 'laboratorio/editar.html', {'form': form, 'laboratorio': laboratorio})

def laboratorio_eliminar(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)

    if laboratorio.medicamentos.exists():
        messages.error(request, 'No se puede eliminar el laboratorio: tiene medicamentos asociados.')
        return redirect('laboratorio_lista')

    if request.method == 'POST':
        try:
            laboratorio.delete()
            messages.success(request, 'Laboratorio eliminado exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el laboratorio: está en uso.')
        return redirect('laboratorio_lista')

    return render(request, 'laboratorio/eliminar.html', {'laboratorio': laboratorio})



def paciente_editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'paciente/editar.html', {'form': form, 'paciente': paciente})

def paciente_eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if paciente.consultas.exists():
        messages.error(request, 'No se puede eliminar el paciente: tiene consultas asociadas.')
        return redirect('paciente_lista')

    if request.method == 'POST':
        try:
            paciente.delete()
            messages.success(request, 'Paciente eliminado exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el paciente: está en uso.')
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
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico creado exitosamente.')
            return redirect('medico_lista')
    else:
        form = MedicoForm()
    return render(request, 'medico/crear.html', {'form': form})


def medico_editar(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico actualizado exitosamente.')
            return redirect('medico_lista')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medico/editar.html', {'form': form, 'medico': medico})


def medico_eliminar(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if medico.consultas.exists():
        messages.error(request, 'No se puede eliminar el médico: tiene consultas asociadas. '
                                )
        return redirect('medico_lista')

    if request.method == 'POST':
        try:
            medico.delete()
            messages.success(request, 'Médico eliminado exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el médico: está en uso.')
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
    consultas = ConsultaMedica.objects.select_related('paciente', 'medico').order_by('-fecha_hora')
    return render(request, 'consulta/lista.html', {'consultas': consultas})

# CREAR
def consulta_crear(request):
    if request.method == 'POST':
        # 1) Buscar FK
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        paciente = get_object_or_404(Paciente, pk=paciente_id, activo=True)
        medico = get_object_or_404(Medico, pk=medico_id, activo=True)

        # 2) Parsear fecha y hora ("YYYY-MM-DDTHH:MM")
        fecha_str = request.POST.get('fecha_hora')  # ej. "2025-10-16T10:30"
        if not fecha_str:
            messages.error(request, 'Debes ingresar la fecha y hora.')
        else:
            try:
                dt = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
                # Si usas USE_TZ=True, vuelve dt consciente
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
            except ValueError:
                messages.error(request, 'Formato de fecha/hora inválido.')
                dt = None

            if dt:
                ConsultaMedica.objects.create(
                    paciente=paciente,
                    medico=medico,
                    fecha_hora=dt,
                    motivo_consulta=request.POST.get('motivo_consulta', '').strip(),
                    diagnostico=request.POST.get('diagnostico', '').strip(),
                    observaciones=request.POST.get('observaciones', '').strip(),
                    estado=request.POST.get('estado', 'AGENDADA'),
                )
                messages.success(request, 'Consulta creada exitosamente.')
                return redirect('consulta_lista')

    # GET o POST con errores → volver a mostrar combos
    pacientes = Paciente.objects.filter(activo=True).order_by('apellido_paterno', 'nombre')
    medicos = Medico.objects.filter(activo=True).order_by('apellido_paterno', 'nombre')
    return render(request, 'consulta/crear.html', {
        'pacientes': pacientes,
        'medicos': medicos,
    })

# EDITAR
def consulta_editar(request, pk):
    consulta = get_object_or_404(ConsultaMedica, pk=pk)

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        paciente = get_object_or_404(Paciente, pk=paciente_id, activo=True)
        medico = get_object_or_404(Medico, pk=medico_id, activo=True)

        fecha_str = request.POST.get('fecha_hora')
        try:
            dt = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
        except ValueError:
            messages.error(request, 'Formato de fecha/hora inválido.')
            dt = None

        if dt:
            consulta.paciente = paciente
            consulta.medico = medico
            consulta.fecha_hora = dt
            consulta.motivo_consulta = request.POST.get('motivo_consulta', '').strip()
            consulta.diagnostico = request.POST.get('diagnostico', '').strip()
            consulta.observaciones = request.POST.get('observaciones', '').strip()
            consulta.estado = request.POST.get('estado', 'AGENDADA')
            consulta.save()
            messages.success(request, 'Consulta actualizada exitosamente.')
            return redirect('consulta_lista')

    pacientes = Paciente.objects.filter(activo=True).order_by('apellido_paterno', 'nombre')
    medicos = Medico.objects.filter(activo=True).order_by('apellido_paterno', 'nombre')
    return render(request, 'consulta/editar.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos,
    })

# ELIMINAR
def consulta_eliminar(request, pk):
    consulta = get_object_or_404(ConsultaMedica, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada.')
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
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento creado exitosamente.')
            return redirect('tratamiento_lista')
    else:
        form = TratamientoForm()
    return render(request, 'tratamiento/crear.html', {'form': form})


def tratamiento_editar(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento actualizado exitosamente.')
            return redirect('tratamiento_lista')
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'tratamiento/editar.html', {'form': form, 'tratamiento': tratamiento})

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
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento creado exitosamente.')
            return redirect('medicamento_lista')
    else:
        form = MedicamentoForm()
    return render(request, 'medicamento/crear.html', {'form': form})


def medicamento_editar(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento actualizado exitosamente.')
            return redirect('medicamento_lista')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'medicamento/editar.html', {'form': form, 'medicamento': medicamento})

def medicamento_eliminar(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)

    if medicamento.recetas.exists():
        messages.error(request, 'No se puede eliminar el medicamento: tiene recetas asociadas.')
        return redirect('medicamento_lista')

    if request.method == 'POST':
        try:
            medicamento.delete()
            messages.success(request, 'Medicamento eliminado exitosamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar el medicamento: está en uso.')
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
    if request.method == 'POST':
        form = RecetaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta médica creada exitosamente.')
            return redirect('receta_lista')
    else:
        form = RecetaMedicaForm()
    return render(request, 'receta/crear.html', {'form': form})


def receta_editar(request, pk):
    receta = get_object_or_404(RecetaMedica, pk=pk)
    if request.method == 'POST':
        form = RecetaMedicaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta médica actualizada exitosamente.')
            return redirect('receta_lista')
    else:
        form = RecetaMedicaForm(instance=receta)
    return render(request, 'receta/editar.html', {'form': form, 'receta': receta})


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