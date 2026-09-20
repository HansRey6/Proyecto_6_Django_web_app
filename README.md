# Gestor de Tareas y Proyectos (Django)

Aplicación web construida con Django que permite a los usuarios registrarse,
autenticarse y gestionar sus propios proyectos y las tareas asociadas a cada
uno.

## Capturas de pantalla 

<img width="1347" height="606" alt="1" src="https://github.com/user-attachments/assets/c5874e05-69a2-4ddd-b0aa-8995196aef0a" />

<img width="1350" height="607" alt="22" src="https://github.com/user-attachments/assets/f464cb87-1f16-45fe-a41e-66b7fa3f3e02" />

<img width="1344" height="592" alt="333" src="https://github.com/user-attachments/assets/eefa28e2-022e-4d54-827c-62f8644c1f0b" />

<img width="1341" height="602" alt="44" src="https://github.com/user-attachments/assets/43768c33-33d9-44e6-85a9-5b8536e5830a" />

## Video de demostración

[Ver video](https://drive.google.com/file/d/17mlMDWL18f2taj6S9QWpcRuZl4X5VQGu/view?usp=sharing)

## Funcionalidades

- Registro de usuarios y autenticación (`django.contrib.auth`).
- Gestión de **proyectos**: crear, ver detalle, editar y eliminar.
- Gestión de **tareas** dentro de cada proyecto: crear, editar, eliminar y
  cambiar de estado (`pendiente`, `en proceso`, `finalizada`).
- Cada usuario solo puede ver y modificar sus propios proyectos y tareas.
- Panel de administración de Django con vistas personalizadas para
  proyectos, tareas y usuarios (incluye conteo de proyectos por usuario).
- Protección CSRF en todos los formularios y validaciones propias (nombres
  de proyecto y títulos de tarea no duplicados, email de registro único).

## Estructura del proyecto

```
django-m-dulo-6/
├── gestor_tareas/          # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py             # URLs raíz (admin, login/logout, registro, tareas.urls)
│   └── wsgi.py / asgi.py
├── tareas/                 # App principal
│   ├── models.py           # Modelos Proyecto y Tarea
│   ├── forms.py            # RegistroUsuarioForm, ProyectoForm, TareaForm
│   ├── views.py            # Vistas basadas en clases (CBVs) con LoginRequiredMixin
│   ├── urls.py              # URLs de proyectos y tareas
│   ├── admin.py             # Registro y personalización del admin
│   ├── tests.py             # Pruebas unitarias de modelos y vistas
│   ├── migrations/          # Migraciones de la app
│   └── templates/
│       ├── base.html
│       ├── registration/    # login.html, registro.html
│       └── tareas/          # templates de proyectos y tareas
├── manage.py
├── requirements.txt
└── db.sqlite3                # Base de datos local (no se versiona en git)
```

## Modelo de datos

- **Proyecto**: pertenece a un `usuario` (FK a `User`). Tiene `nombre`,
  `descripcion` y `fecha_creacion`.
- **Tarea**: pertenece a un `Proyecto` (FK). Tiene `titulo`, `descripcion`,
  `estado` (con opciones) y `fecha_creacion`.

Un usuario puede tener varios proyectos, y cada proyecto puede tener varias
tareas.

## Instalación y puesta en marcha

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd django-m-dulo-6
   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones**

   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario** (para acceder al panel `/admin/`)

   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo**

   ```bash
   python manage.py runserver
   ```

   La aplicación queda disponible en `http://127.0.0.1:8000/`.

## Uso

- `/` — lista de proyectos del usuario autenticado (requiere login).
- `/registro/` — crear una cuenta nueva.
- `/accounts/login/` y `/accounts/logout/` — iniciar y cerrar sesión.
- `/proyectos/nuevo/` — crear un proyecto.
- `/proyectos/<id>/` — detalle de un proyecto y sus tareas.
- `/proyectos/<id>/editar/` y `/proyectos/<id>/eliminar/`.
- `/proyectos/<id>/tareas/nueva/` — crear una tarea dentro de ese proyecto.
- `/tareas/<id>/editar/` y `/tareas/<id>/eliminar/`.
- `/admin/` — panel de administración de Django.

## Ejecutar las pruebas

```bash
python manage.py test
```

Las pruebas cubren:
- Los modelos `Proyecto` y `Tarea` (`__str__`, `get_absolute_url`, valores
  por defecto).
- El registro de usuarios, incluyendo el rechazo de emails duplicados.
- Que las vistas protegidas redirijan a login si no hay sesión.
- Que un usuario no pueda ver, editar ni crear tareas en proyectos de otro
  usuario (control de acceso).
- El CRUD completo de proyectos y tareas, incluyendo las validaciones de
  nombres/títulos duplicados.

## Notas de seguridad implementadas

- Todas las vistas de proyectos y tareas usan `LoginRequiredMixin`.
- Los `queryset` de cada vista se filtran siempre por el usuario autenticado
  (`usuario=self.request.user` o `proyecto__usuario=self.request.user`), de
  modo que acceder a un ID de otro usuario devuelve `404` en vez de exponer
  datos ajenos.
- Todos los formularios incluyen `{% csrf_token %}`.
- Las contraseñas se validan con los validadores estándar de Django
  (`AUTH_PASSWORD_VALIDATORS`).
