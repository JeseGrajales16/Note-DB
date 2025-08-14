from django.urls import path
from .views import RegistroUsuarioView, ListarUsuariosView, EliminarUsuarioView

urlpatterns = [
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("usuarios/", ListarUsuariosView.as_view(), name="usuarios"),
    path("usuarios/eliminar/<int:pk>/", EliminarUsuarioView.as_view(), name="eliminar_usuario"),
]
