from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Proyecto, Tarea


class ProyectoModelTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="ana", password="clave12345")
        self.proyecto = Proyecto.objects.create(usuario=self.usuario, nombre="Tesis")

    def test_str_devuelve_el_nombre(self):
        self.assertEqual(str(self.proyecto), "Tesis")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.proyecto.get_absolute_url(),
            reverse("proyecto_detail", kwargs={"pk": self.proyecto.pk}),
        )


class TareaModelTest(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(username="ana", password="clave12345")
        self.proyecto = Proyecto.objects.create(usuario=usuario, nombre="Tesis")
        self.tarea = Tarea.objects.create(proyecto=self.proyecto, titulo="Capítulo 1")

    def test_str_devuelve_el_titulo(self):
        self.assertEqual(str(self.tarea), "Capítulo 1")

    def test_estado_por_defecto_es_pendiente(self):
        self.assertEqual(self.tarea.estado, "pendiente")


class RegistroViewTest(TestCase):
    def test_registro_crea_usuario_y_lo_autentica(self):
        respuesta = self.client.post(reverse("registro"), {
            "username": "nuevo",
            "email": "nuevo@example.com",
            "password1": "ClaveSegura123",
            "password2": "ClaveSegura123",
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(User.objects.filter(username="nuevo").exists())
        # El usuario queda logueado tras registrarse (ver RegistroView.form_valid)
        self.assertTrue(respuesta.wsgi_request.user.is_authenticated)

    def test_registro_rechaza_email_duplicado(self):
        User.objects.create_user(username="existente", email="repetido@example.com", password="claveOtra123")
        respuesta = self.client.post(reverse("registro"), {
            "username": "otro",
            "email": "repetido@example.com",
            "password1": "ClaveSegura123",
            "password2": "ClaveSegura123",
        })
        self.assertEqual(respuesta.status_code, 200)  # se re-renderiza el form con error
        self.assertFalse(User.objects.filter(username="otro").exists())


class AccesoRequiereLoginTest(TestCase):
    def test_lista_de_proyectos_redirige_a_login_si_no_hay_sesion(self):
        respuesta = self.client.get(reverse("proyecto_list"))
        self.assertRedirects(
            respuesta, f"{reverse('login')}?next={reverse('proyecto_list')}"
        )

    def test_crear_proyecto_redirige_a_login_si_no_hay_sesion(self):
        respuesta = self.client.get(reverse("proyecto_create"))
        self.assertEqual(respuesta.status_code, 302)


class ProyectoCRUDTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="ana", password="clave12345")
        self.client.login(username="ana", password="clave12345")

    def test_crear_proyecto(self):
        respuesta = self.client.post(reverse("proyecto_create"), {
            "nombre": "Nuevo proyecto",
            "descripcion": "Descripción de prueba",
        })
        self.assertEqual(respuesta.status_code, 302)
        proyecto = Proyecto.objects.get(nombre="Nuevo proyecto")
        self.assertEqual(proyecto.usuario, self.usuario)

    def test_no_permite_nombres_de_proyecto_duplicados_para_el_mismo_usuario(self):
        Proyecto.objects.create(usuario=self.usuario, nombre="Tesis")
        respuesta = self.client.post(reverse("proyecto_create"), {
            "nombre": "Tesis",
            "descripcion": "",
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Proyecto.objects.filter(usuario=self.usuario, nombre="Tesis").count(), 1)

    def test_lista_proyectos_solo_muestra_los_del_usuario_logueado(self):
        otro_usuario = User.objects.create_user(username="beto", password="clave12345")
        Proyecto.objects.create(usuario=self.usuario, nombre="Mío")
        Proyecto.objects.create(usuario=otro_usuario, nombre="Ajeno")

        respuesta = self.client.get(reverse("proyecto_list"))

        self.assertContains(respuesta, "Mío")
        self.assertNotContains(respuesta, "Ajeno")

    def test_no_puede_ver_detalle_de_proyecto_ajeno(self):
        otro_usuario = User.objects.create_user(username="beto", password="clave12345")
        proyecto_ajeno = Proyecto.objects.create(usuario=otro_usuario, nombre="Ajeno")

        respuesta = self.client.get(reverse("proyecto_detail", kwargs={"pk": proyecto_ajeno.pk}))

        self.assertEqual(respuesta.status_code, 404)

    def test_eliminar_proyecto(self):
        proyecto = Proyecto.objects.create(usuario=self.usuario, nombre="Para borrar")
        respuesta = self.client.post(reverse("proyecto_delete", kwargs={"pk": proyecto.pk}))
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Proyecto.objects.filter(pk=proyecto.pk).exists())


class TareaCRUDTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="ana", password="clave12345")
        self.client.login(username="ana", password="clave12345")
        self.proyecto = Proyecto.objects.create(usuario=self.usuario, nombre="Tesis")

    def test_crear_tarea_en_proyecto_propio(self):
        respuesta = self.client.post(
            reverse("tarea_create", kwargs={"proyecto_id": self.proyecto.pk}),
            {"titulo": "Escribir intro", "descripcion": "", "estado": "pendiente"},
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Tarea.objects.filter(proyecto=self.proyecto, titulo="Escribir intro").exists())

    def test_no_puede_crear_tarea_en_proyecto_ajeno(self):
        otro_usuario = User.objects.create_user(username="beto", password="clave12345")
        proyecto_ajeno = Proyecto.objects.create(usuario=otro_usuario, nombre="Ajeno")

        respuesta = self.client.post(
            reverse("tarea_create", kwargs={"proyecto_id": proyecto_ajeno.pk}),
            {"titulo": "Intrusa", "descripcion": "", "estado": "pendiente"},
        )

        self.assertEqual(respuesta.status_code, 404)
        self.assertFalse(Tarea.objects.filter(titulo="Intrusa").exists())

    def test_no_permite_titulos_de_tarea_duplicados_en_el_mismo_proyecto(self):
        Tarea.objects.create(proyecto=self.proyecto, titulo="Capítulo 1")
        respuesta = self.client.post(
            reverse("tarea_create", kwargs={"proyecto_id": self.proyecto.pk}),
            {"titulo": "Capítulo 1", "descripcion": "", "estado": "pendiente"},
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Tarea.objects.filter(proyecto=self.proyecto, titulo="Capítulo 1").count(), 1)

    def test_actualizar_estado_de_tarea(self):
        tarea = Tarea.objects.create(proyecto=self.proyecto, titulo="Capítulo 1")
        respuesta = self.client.post(
            reverse("tarea_update", kwargs={"pk": tarea.pk}),
            {"titulo": "Capítulo 1", "descripcion": "", "estado": "finalizada"},
        )
        self.assertEqual(respuesta.status_code, 302)
        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, "finalizada")
