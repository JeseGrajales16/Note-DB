from django.urls import path
from .views import RegistroUsuarioView, ListarUsuariosView, EliminarUsuarioView, CursoRegistroView, ListarCursosView, EliminarCursoView, MateriaRegistroView,ListarMateriasView,EliminarMateriasView,AsistenciaRegistroView,ListarAsistenciasView,EliminarAsistenciasView

urlpatterns = [
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("usuarios/", ListarUsuariosView.as_view(), name="usuarios"),
    path("usuarios/eliminar/<int:pk>/", EliminarUsuarioView.as_view(), name="eliminar_usuario"),
    path("registrar_curso/", CursoRegistroView.as_view(), name="registrar_curso" ),
    path("listar_cursos/", ListarCursosView.as_view(), name="listar_cursos"),
    path("cursos/eliminar/<int:pk>/", EliminarCursoView.as_view(), name="eliminar_curso"),
    path("registrar_materias/", MateriaRegistroView.as_view(), name="registrar_materias" ),
    path("listar_de_materias/", ListarMateriasView.as_view(), name="listar_materias"),
    path("materias/eliminar/<int:pk>/", EliminarMateriasView.as_view(), name="eliminar_materias"),
    path("registrar_materias/", AsistenciaRegistroView.as_view(), name="registrar_asistencias" ),
    path("listar_de_asistencias/", ListarCursosView.as_view(), name="listar_asistencias" ),
    path("asistencias/eliminar/<int:pk>/",EliminarAsistenciasView.as_view(), name="eliminar_asistencias"),
]
