# SaludCerca

Sitio web académico para organizar información sobre atención médica y desarrollar un flujo de consulta de especialidades y solicitud de citas. El proyecto utiliza Django y Django REST Framework.

## Estructura

| Carpeta | Responsabilidad |
|---|---|
| `config/` | Configuración del proyecto, rutas y vista de inicio |
| `templates/` | Plantilla HTML de la página principal |
| `static/css/` | Estilos y diseño responsive |
| `static/js/` | Navegación móvil y búsqueda de especialidades |
| `usuarios/` | Usuarios y pacientes |
| `medicos/` | Centros médicos, doctores, especialidades y horarios |
| `citas/` | Citas y reseñas |
| `notificaciones/` | Notificaciones y configuraciones |
| `docs/` | Bitácora del avance 2 |

## Requisitos

- Python compatible con la versión de Django declarada en `requirements.txt`
- Git

## Instalación en Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Edita `.env` y configura `SECRET_KEY` y `DEBUG` para tu entorno local. La base de datos predeterminada es SQLite, por lo que no necesitas instalar PostgreSQL para ejecutar la configuración local.

## Rutas principales

- Página principal: <http://127.0.0.1:8000/>
- Panel administrativo: <http://127.0.0.1:8000/admin/>
- API navegable: <http://127.0.0.1:8000/api/>
- Inicio de sesión de la API navegable: <http://127.0.0.1:8000/api-auth/login/>

La página inicial incluye navegación adaptable, tarjetas de especialidades con filtrado por texto y enlaces a la API. Las especialidades mostradas son contenido de ejemplo; la conexión dinámica con los registros reales está pendiente.

## API

Los routers agrupan los recursos por aplicación. Los endpoints disponibles incluyen usuarios, pacientes, centros, especialidades, doctores, horarios, citas, reseñas, notificaciones y configuraciones. La API utiliza autenticación por sesión y Basic Auth para desarrollo.

Consulta `docs/bitacora_avance_2.md` para el registro del avance funcional y las tareas pendientes.
