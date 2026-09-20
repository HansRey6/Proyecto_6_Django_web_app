from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Proyecto, Tarea

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.setdefault("class", "form-control")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con ese email.")
        return email


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        # El usuario se pasa desde la vista para poder validar duplicados
        # sin tocar el modelo (el dueño se asigna en la vista, no en el form).
        self.usuario = usuario
        super().__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre:
            raise forms.ValidationError("El nombre del proyecto no puede estar vacío.")
        if self.usuario is not None:
            duplicado = Proyecto.objects.filter(usuario=self.usuario, nombre__iexact=nombre)
            if self.instance.pk:
                duplicado = duplicado.exclude(pk=self.instance.pk)
            if duplicado.exists():
                raise forms.ValidationError("Ya tienes un proyecto con ese nombre.")
        return nombre


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "estado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, proyecto=None, **kwargs):
        self.proyecto = proyecto
        super().__init__(*args, **kwargs)

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if not titulo:
            raise forms.ValidationError("El título de la tarea no puede estar vacío.")
        if self.proyecto is not None:
            duplicado = Tarea.objects.filter(proyecto=self.proyecto, titulo__iexact=titulo)
            if self.instance.pk:
                duplicado = duplicado.exclude(pk=self.instance.pk)
            if duplicado.exists():
                raise forms.ValidationError("Ya existe una tarea con ese título en este proyecto.")
        return titulo