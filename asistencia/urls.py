from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("usuarios/", ListarUsuariosView.as_view(), name="usuarios"),
    path("usuarios/eliminar/<int:pk>/", EliminarUsuarioView.as_view(), name="eliminar_usuario"),
    path("registrar_curso/", CursoRegistroView.as_view(), name="registrar_curso" ),
    path("cursos/", ListarCursosView.as_view(), name="listar_cursos"),
    path("cursos/eliminar/<int:pk>/", EliminarCursoView.as_view(), name="eliminar_curso"),
    path("registrar_materia/", MateriaRegistroView.as_view(), name="registrar_materia" ),
    path("materias/", ListarMateriasView.as_view(), name="listar_materias"),
    path("materias/eliminar/<int:pk>/", EliminarMateriasView.as_view(), name="eliminar_materia"),
    path("asistencias/", ListarCursosView.as_view(), name="listar_asistencias" ),
    path("registrar_horario/", HorarioRegistroView.as_view(), name="registrar_horario" ),
    path("horarios/", ListarHorariosView.as_view(), name="listar_horarios"),
    path("horario/eliminar/<int:pk>/", EliminarHorarioView.as_view(), name="eliminar_horario"),
    path("mi-horario/", MiHorarioView.as_view(), name="horario"),
    path("mi-horario-profesor/", MiHorarioProfesorView.as_view(), name="horario_profesor"),
    path('asistencia/tomar/<int:horario_id>/<str:fecha>/', TomarAsistenciaView.as_view(), name='tomar_asistencia'),
    path('horarios-acudiente/', HorariosAcudienteView.as_view(), name='horarios_acudiente'),
    path("eventos/", TemplateView.as_view(template_name="eventos_generales.html"), name="eventos_generales"),
    path("eventos/exalumnos/", TemplateView.as_view(template_name="eventos_exalumnos.html"), name="eventos_exalumnos"),
]
