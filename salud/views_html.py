# salud/views_html.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Especialidad
from .forms import EspecialidadForm

class EspecialidadListView(ListView):
    model = Especialidad
    template_name = "salud/especialidad_list.html"

class EspecialidadCreateView(CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "salud/especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")

class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "salud/especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    template_name = "salud/especialidad_confirm_delete.html"
    success_url = reverse_lazy("especialidad_list")
