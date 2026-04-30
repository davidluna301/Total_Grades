# Total_Grades

<p align="center">
	<img src="./Total_Grades_logo.png" alt="Total Grades logo" width="220">
</p>

<https://total-grades.onrender.com>

Aplicacion web desarrollada con Django para gestionar calificaciones de estudiantes con autenticacion por roles, paneles diferenciados y operaciones CRUD sobre notas.

## Descripcion general

Total_Grades permite administrar y consultar notas academicas desde una unica plataforma. El sistema define tres tipos de usuario:

- `superadmin`: vista global del sistema y control total del CRUD.
- `profesor`: gestion de notas y consulta de indicadores academicos.
- `estudiante`: consulta de sus propias materias y promedio personal.

La aplicacion calcula automaticamente el promedio de cada registro a partir de tres notas con rango valido entre `0.00` y `5.00`.

## Funcionalidades

### Autenticacion y acceso

- Inicio de sesion con usuario y contrasena.
- Redireccion automatica a la interfaz correspondiente segun el rol.
- Cierre de sesion.
- Restriccion de vistas por permisos usando roles de Django.

### Funcionalidades por rol

#### Superadmin

- Acceso al panel administrativo principal.
- Visualizacion de metricas globales.
- Crear calificaciones.
- Editar calificaciones.
- Eliminar calificaciones.
- Consultar listado general de notas.
- Consultar promedio general del sistema.

#### Profesor

- Acceso al panel del profesor.
- Crear calificaciones.
- Editar calificaciones.
- Consultar listado general de notas.
- Consultar promedio general.
- Ver materias activas y registros recientes.

#### Estudiante

- Acceso al panel del estudiante.
- Ver solo sus propias calificaciones.
- Consultar su promedio personal.
- Consultar la cantidad de materias registradas.

## Tecnologias utilizadas

- Python
- Django 6
- SQLite para entorno local
- PostgreSQL para despliegue en Render
- WhiteNoise para archivos estaticos en produccion
- Gunicorn como servidor WSGI

## Estructura funcional

- Pagina principal: presenta el sistema y acceso al login.
- Login: valida credenciales y redirige al panel del rol.
- Paneles por rol: superadmin, profesor y estudiante.
- Modulo de calificaciones: listado, creacion, edicion, eliminacion y promedio general.

## Instalacion local

### 1. Clonar el repositorio

```bash
git clone https://github.com/davidluna301/Total_Grades.git
cd Total_Grades
```

### 2. Crear y activar entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Cargar usuarios y datos de ejemplo

```bash
python manage.py seed_db --grades
```

### 6. Iniciar el servidor local

```bash
python manage.py runserver
```

Accede desde:

```text
http://127.0.0.1:8000/
```

## Pasos para ingresar al sistema

### 1. Abrir la aplicacion

- Local: `http://127.0.0.1:8000/`
- Produccion: la URL publica del servicio en Render

### 2. Entrar al formulario de login

- Haz clic en el acceso principal.
- Ingresa usuario y contrasena.

### 3. Usar una cuenta valida

Credenciales demo principales:

- `superadmin` / `SuperAdmin2026!`
- `profesor1` / `Profesor2026!`
- `ID00001` / `Estudiante2026!01`

El proyecto incluye mas cuentas demo en [usuarios_y_contrasenas.txt](usuarios_y_contrasenas.txt).

### 4. Validacion del acceso

- Si las credenciales son correctas, el sistema inicia sesion.
- El usuario es enviado automaticamente a su panel.
- Si no tiene permisos para una vista, es redirigido a su dashboard.

## Rutas principales

- `/` : pagina de inicio
- `/login/` : inicio de sesion
- `/logout/` : cierre de sesion
- `/panel/` : redireccion al dashboard segun rol
- `/panel/superadmin/` : panel del superadmin
- `/panel/profesor/` : panel del profesor
- `/panel/estudiante/` : panel del estudiante
- `/calificaciones/` : listado de calificaciones
- `/calificaciones/crear/` : crear calificacion
- `/calificaciones/editar/<id>/` : editar calificacion
- `/calificaciones/eliminar/<id>/` : eliminar calificacion
- `/calificaciones/promedio-general/` : promedio general

## Modelo de datos

La entidad principal es `Calificacion`, que almacena:

- `nombre_estudiante`
- `identificacion`
- `asignatura`
- `nota1`
- `nota2`
- `nota3`
- `promedio`

El promedio se calcula automaticamente al guardar el registro.

## Despliegue en Render

<https://total-grades.onrender.com>

El proyecto esta preparado para usar PostgreSQL en Render mediante la variable `DATABASE_URL`.

### Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

### Start Command

```bash
bash start.sh
```

El archivo `start.sh` ejecuta:

1. Migraciones.
2. Siembra de usuarios y calificaciones demo.
3. Arranque de Gunicorn.

## Variables de entorno recomendadas

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`

## Datos demo incluidos

El comando `python manage.py seed_db --grades` crea:

- 1 superadmin
- 2 profesores
- 20 estudiantes
- 20 registros de calificaciones de ejemplo

## Estado actual del proyecto

- Login con redireccion por rol
- CRUD de calificaciones
- Seed automatico para usuarios demo
- Soporte local con SQLite
- Soporte de produccion con PostgreSQL en Render
