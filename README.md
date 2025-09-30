# Sistema de Gestión Académica y Asistencia

*Aplicación web desarrollada con Django para la gestión de estudiantes, profesores, horarios y asistencias de una institución educativa.*

## Descripción

Este proyecto es una plataforma web integral diseñada para modernizar y centralizar la gestión académica. Permite administrar diferentes roles de usuario (profesores, estudiantes, acudientes), crear y organizar la estructura académica (cursos, materias, horarios) y llevar un registro detallado y en tiempo real de la asistencia de los estudiantes.

La aplicación cuenta con una interfaz moderna y reactiva, utilizando AJAX para operaciones de creación y eliminación sin necesidad de recargar la página, y envía notificaciones automáticas para mantener informada a la comunidad educativa.

## ✨ Características Principales

### Gestión de Usuarios y Roles

  - **Autenticación de Usuarios:** Sistema de inicio y cierre de sesión seguro.
  - **Registro por Roles:** Formulario de registro dinámico que solicita información específica según el rol seleccionado (Profesor, Estudiante, Acudiente, Exalumno).
  - **Protección de Vistas:** Acceso a las diferentes secciones restringido según el rol del usuario. Un estudiante no puede acceder a las herramientas de administración, por ejemplo.

### Gestión Académica (CRUD)

  - **Administración completa** (Crear, Leer, Actualizar, Eliminar) para:
      - **Cursos:** (ej. "Grado 601", "Grado 10A").
      - **Materias:** Asignadas a un curso y un profesor específico.
      - **Horarios:** Creación de un horario general con validación para evitar conflictos (un profesor o un curso no pueden tener dos clases a la misma hora).
  - **Interfaz Moderna:** Todas las operaciones de gestión se realizan a través de **ventanas modales (pop-ups)** y **AJAX**, proporcionando una experiencia de usuario fluida y sin recargas de página.

### Sistema de Horarios

  - **Horario Personalizado por Rol:**
      - **Estudiantes:** Ven su horario semanal personal, con las celdas coloreadas según su estado de asistencia.
      - **Profesores:** Ven su horario semanal de clases, indicando qué materia dictan en qué curso. Las celdas se colorean de verde si ya han tomado la asistencia para esa clase.
      - **Acudientes:** Ven los horarios semanales de todos los estudiantes que tienen a su cargo.
  - **Navegación Semanal:** Todos los horarios permiten navegar a semanas anteriores y siguientes, y volver fácilmente a la semana actual.

### Sistema de Asistencia

  - **Toma de Asistencia Intuitiva:** El profesor accede a una lista de estudiantes por clase y puede marcar el estado de cada uno (`Presente`, `Ausente`, `Tarde`, `Excusa`) con botones visuales.
  - **Registro Persistente:** La asistencia se guarda por fecha, permitiendo al docente registrar o corregir la asistencia de días anteriores.
  - **Notificaciones Automáticas:** Cuando un profesor marca a un estudiante como **ausente**, el sistema envía automáticamente un **correo electrónico al acudiente** registrado.

### Módulo de Eventos

  - **Eventos Generales:** Una sección pública visible para todos los visitantes (registrados o no) con información sobre eventos de la institución.
  - **Información para Exalumnos:** Una sección de contenido estático y exclusivo que solo es visible para los usuarios con el rol de "Exalumno".

## 🛠️ Tecnologías Utilizadas

  - **Backend:** Python, Django
  - **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
  - **Framework CSS:** Bootstrap 5
  - **Base de Datos:** PostgreSQL (configurable en `settings.py`)


## 🚀 Instalación y Puesta en Marcha (con Docker)

Sigue estos pasos para ejecutar el proyecto utilizando Docker. Esto asegura un entorno de desarrollo consistente y autocontenido.

### 1\. Prerrequisitos

  - Docker
  - Docker Compose

### 2\. Clonar el Repositorio

```bash
git clone https://github.com/JeseGrajales16/Note-DB.git
cd Note-DB
```

### 3\. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto. Docker Compose lo usará para configurar los contenedores. Este archivo **no** debe ser subido a Git.

Y añade las variables respectivas.

### 4\. Construir y Ejecutar los Contenedores

Este comando construirá la imagen de tu aplicación Django y la iniciará junto con la base de datos.

```bash
docker-compose up --build
```

La primera vez puede tardar unos minutos. Después de que termine, deja esta terminal abierta.

### 5\. Ejecutar Migraciones

Abre una **segunda terminal** en la misma carpeta del proyecto y ejecuta el siguiente comando para crear las tablas en la base de datos que se está ejecutando dentro del contenedor.

```bash
docker-compose exec django_app manage.py migrate
```

### 6\. Crear un Superusuario

En la misma segunda terminal, crea un usuario administrador para acceder al panel de Django (`/admin`).

```bash
docker-compose exec django_app manage.py createsuperuser
```

¡Y listo\! La aplicación estará disponible en tu navegador en `http://localhost:8000`.

-----

## Uso Diario

  - **Para iniciar la aplicación:** `docker-compose up`
  - **Para detener la aplicación:** `docker-compose down`
  - **Para ejecutar cualquier otro comando de `manage.py`:** `docker-compose exec django_app manage.py <comando>` (ej. `makemigrations`)