from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("usuarios/", ListarUsuariosView.as_view(), name="usuarios"),
    path("usuarios/eliminar/<int:pk>/", EliminarUsuarioView.as_view(), name="eliminar_usuario"),
    path("registrar_curso/", CursoRegistroView.as_view(), name="registrar_curso" ),
    path("cursos/", ListarCursosView.as_view(), name="listar_cursos"),
    path("cursos/eliminar/<int:pk>/", EliminarCursoView.as_view(), name="eliminar_curso"),
    path("registrar_materia/", MateriaRegistroView.as_view(), name="registrar_materia" ),
    path("materias/", ListarMateriasView.as_view(), name="listar_materias"),
    path("materias/eliminar/<int:pk>/", EliminarMateriasView.as_view(), name="eliminar_materia"),
    path("registrar_asistencia/", AsistenciaRegistroView.as_view(), name="registrar_asistencias" ),
    path("asistencias/", ListarCursosView.as_view(), name="listar_asistencias" ),
    # path("asistencias/eliminar/<int:pk>/",EliminarAsistenciasView.as_view(), name="eliminar_asistencias"),
    path("registrar_horario/", HorarioRegistroView.as_view(), name="registrar_horario" ),
    path("lista_horario/", ListasHorarioView.as_view(), name="lista_de_horarios"),
    path("horario/eliminar/<int:pk>/", EliminarHorarioView.as_view(), name="eliminar_horario"),
]
