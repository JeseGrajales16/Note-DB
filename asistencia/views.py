from django.views.generic import ListView, DeleteView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import User, Curso, Materia, Asistencia, Horario
from .forms import UsuarioRegistroForm,CursoRegistroForm,MateriaRegistroForm,AsistanciaRegistroFrom,HorarioRegistroForm

class HomeView(TemplateView):
    template_name= "home.html"
    success_url= reverse_lazy("home")


class RegistroUsuarioView(CreateView):
    model = User
    form_class = UsuarioRegistroForm
    template_name = "registro.html"
    success_url = reverse_lazy("usuarios")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class ListarUsuariosView(ListView):
    model = User
    template_name = "usuarios.html"
    context_object_name = "usuarios"


class EliminarUsuarioView(DeleteView):
    model = User
    template_name = "eliminar_usuario.html"
    success_url = reverse_lazy("usuarios")


class CursoRegistroView(CreateView):
    model = Curso
    form_class = CursoRegistroForm
    template_name ="curso_registro.html"
    success_url = reverse_lazy("listar_cursos")


class ListarCursosView(ListView):
    model = Curso 
    template_name = "listar_cursos.html"
    context_object_name = "cursos"


class EliminarCursoView(DeleteView):
    model = Curso
    template_name = "eliminar_curso.html"
    success_url = reverse_lazy("listar_cursos")


class MateriaRegistroView(CreateView): 
    model = Materia
    form_class = MateriaRegistroForm
    template_name = "materias_registro.html"
    success_url = reverse_lazy("listar_materias")


class ListarMateriasView(ListView):
    model = Materia 
    template_name = "lista_de_materias.html"
    context_object_name = "materias"


class EliminarMateriasView(DeleteView):
    model = Materia
    template_name = "eliminar_materias.html"
    success_url = reverse_lazy("listar_materias")


class AsistenciaRegistroView(CreateView):
    model = Asistencia
    form_class = AsistanciaRegistroFrom
    template_name = "asistencias_registro.html"
    success_url = reverse_lazy("asistencias")


class ListarAsistenciasView(ListView):
    model = Asistencia 
    template_name = "lista_de_asistencias.html"
    context_object_name = "asistencias"


class HorarioRegistroView(CreateView):
    model = Horario
    form_class = HorarioRegistroForm
    template_name = "registro_horario.html"
    success_url = reverse_lazy("lista_de_horarios")


class ListasHorarioView(ListView):
    model = Horario
    template_name = "lista_horarios.html"
    context_object_name = "horarios"


class EliminarHorarioView(DeleteView):
    model = Horario
    template_name = "eliminar_horario.html"
    success_url = reverse_lazy("lista_de_horarios")

    

    
