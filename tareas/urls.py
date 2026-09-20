from django.urls import path

from .views import (ProyectoCreateView, ProyectoDeleteView, ProyectoDetailView, ProyectoListView, ProyectoUpdateView, TareaCreateView, TareaDeleteView, TareaUpdateView,)

urlpatterns = [
    path("", ProyectoListView.as_view(), name="proyecto_list"),
    path("proyectos/nuevo/", ProyectoCreateView.as_view(), name="proyecto_create"),
    path("proyectos/<int:pk>/", ProyectoDetailView.as_view(), name="proyecto_detail"),
    path("proyectos/<int:pk>/editar/", ProyectoUpdateView.as_view(), name="proyecto_update"),
    path("proyectos/<int:pk>/eliminar/", ProyectoDeleteView.as_view(), name="proyecto_delete"),
    path("proyectos/<int:proyecto_id>/tareas/nueva/", TareaCreateView.as_view(), name="tarea_create"),
    path("tareas/<int:pk>/editar/", TareaUpdateView.as_view(), name="tarea_update"),
    path("tareas/<int:pk>/eliminar/", TareaDeleteView.as_view(), name="tarea_delete"),
]