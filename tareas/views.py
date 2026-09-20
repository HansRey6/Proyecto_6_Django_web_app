from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProyectoForm, RegistroUsuarioForm, TareaForm
from .models import Proyecto, Tarea

class RegistroView(CreateView):
    template_name = "registration/registro.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy("proyecto_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "tareas/proyecto_list.html"
    context_object_name = "proyectos"

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = "tareas/proyecto_detail.html"
    context_object_name = "proyecto"

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = "tareas/proyecto_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = "tareas/proyecto_form.html"

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs


class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = "tareas/proyecto_confirm_delete.html"
    success_url = reverse_lazy("proyecto_list")

    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = "tareas/tarea_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(
            Proyecto,
            pk=self.kwargs["proyecto_id"],
            usuario=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["proyecto"] = self.proyecto
        return kwargs

    def form_valid(self, form):
        form.instance.proyecto = self.proyecto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("proyecto_detail", kwargs={"pk": self.proyecto.pk})


class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = "tareas/tarea_form.html"

    def get_queryset(self):
        return Tarea.objects.filter(proyecto__usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["proyecto"] = self.object.proyecto
        return kwargs

    def get_success_url(self):
        return reverse("proyecto_detail", kwargs={"pk": self.object.proyecto.pk})


class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = "tareas/tarea_confirm_delete.html"

    def get_queryset(self):
        return Tarea.objects.filter(proyecto__usuario=self.request.user)

    def get_success_url(self):
        return reverse("proyecto_detail", kwargs={"pk": self.object.proyecto.pk})