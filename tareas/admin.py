from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Proyecto, Tarea

class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 0

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "fecha_creacion")
    search_fields = ("nombre", "usuario__username")
    list_filter = ("usuario",)
    inlines = [TareaInline]

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "proyecto", "estado", "fecha_creacion")
    list_filter = ("estado", "proyecto")
    search_fields = ("titulo", "proyecto__nombre")


class ProyectoInline(admin.TabularInline):
    model = Proyecto
    extra = 0
    fields = ("nombre", "fecha_creacion")
    readonly_fields = ("fecha_creacion",)
    show_change_link = True


class GestorUserAdmin(UserAdmin):
    """
    Extiende el admin de usuarios por defecto para que, además de gestionar
    permisos y grupos (ya incluido en UserAdmin), se puedan ver de un
    vistazo los proyectos de cada usuario.
    """
    list_display = UserAdmin.list_display + ("cantidad_proyectos",)
    inlines = [ProyectoInline]

    @admin.display(description="Proyectos")
    def cantidad_proyectos(self, obj):
        return obj.proyectos.count()


admin.site.unregister(User)
admin.site.register(User, GestorUserAdmin)