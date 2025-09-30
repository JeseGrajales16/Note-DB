# 1. Importaciones de la Librería Estándar de Python
from datetime import date, timedelta
# 2. Importaciones de Paquetes de Terceros (Django)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView
# 3. Importaciones de la Aplicación Local
from .forms import (
    CursoRegistroForm,
    CustomLoginForm,
    HorarioRegistroForm,
    MateriaRegistroForm,
    UsuarioRegistroForm,
)
from .models import (
    Acudiente,
    Asistencia,
    Curso,
    Estudiante,
    Exalumno,
    Horario,
    Materia,
    Profesor,
    User,
)


def construir_horario_semanal(horarios_base, asistencias_semana, inicio_semana):
    """
    Función que toma una lista de horarios y asistencias y devuelve un
    diccionario estructurado por fecha para la semana dada.
    """
    mapa_asistencias_estudiante = {(a.horario.id, a.fecha): a.estado for a in asistencias_semana}
    asistencias_tomadas_profesor = set(asistencias_semana.values_list('horario_id', 'fecha'))
    
    DIA_MAP = {'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3, 'Viernes': 4}
    
    dias_semana_fechas = [(inicio_semana + timedelta(days=i)) for i in range(5)]
    horario_semanal = {dia: [] for dia in dias_semana_fechas}

    for horario in horarios_base:
        dia_numerico_horario = DIA_MAP.get(horario.dia_semana)
        if dia_numerico_horario is not None:
            fecha_de_clase = inicio_semana + timedelta(days=dia_numerico_horario)
            
            estado_estudiante = mapa_asistencias_estudiante.get((horario.id, fecha_de_clase))
            asistencia_tomada = (horario.id, fecha_de_clase) in asistencias_tomadas_profesor
            
            horario_semanal[fecha_de_clase].append({
                'horario': horario,
                'estado': estado_estudiante,
                'asistencia_tomada': asistencia_tomada,
            })
    return horario_semanal


class HorarioSemanalMixin:
    """
    Mixin simplificado que calcula las fechas y llama a la función de ayuda.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        fecha_str = self.request.GET.get('fecha')
        hoy = date.fromisoformat(fecha_str) if fecha_str else timezone.now().date()
        
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=4)
        
        horarios_base = self.get_horarios_base()
        asistencias_semana = self.get_asistencias_semana(inicio_semana, fin_semana)

        # Usamos la nueva función de ayuda
        context['horario_semanal'] = construir_horario_semanal(horarios_base, asistencias_semana, inicio_semana)
        
        context['semana_anterior'] = inicio_semana - timedelta(days=7)
        context['semana_siguiente'] = inicio_semana + timedelta(days=7)
        context['semana_actual_str'] = f"{inicio_semana.strftime('%d/%m/%Y')} - {fin_semana.strftime('%d/%m/%Y')}"
        
        return context
    

class ProfesorRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el usuario logueado es un profesor.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'profesor'
    

class EstudianteRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el usuario logueado es un estudiante.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'estudiante'
    

class AcudienteRequiredMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el usuario logueado es un acudiente.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'acudiente'
    

class HomeView(TemplateView):
    template_name= "home.html"
    success_url= reverse_lazy("home")


class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True  # si ya está logueado, lo redirige


class CustomLogoutView(LogoutView):
    next_page = "home"  # redirige a home después de cerrar sesión


class RegistroUsuarioView(LoginRequiredMixin, ProfesorRequiredMixin, CreateView):
    model = User
    form_class = UsuarioRegistroForm
    template_name = "registro.html"
    success_url = reverse_lazy("usuarios")

    def form_valid(self, form):
        # 1. Creamos el objeto User pero sin guardarlo aún en la BD
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save() # Ahora sí guardamos el User

        # 2. Leemos el rol y los datos adicionales del formulario
        rol = form.cleaned_data.get('rol')
        
        # 3. Creamos el perfil correspondiente al rol
        if rol == 'profesor':
            Profesor.objects.create(usuario=user)
        
        elif rol == 'estudiante':
            curso = form.cleaned_data.get('curso')
            acudiente_user = form.cleaned_data.get('acudiente')
            
            # Buscamos o creamos el perfil del acudiente
            acudiente_obj, created = Acudiente.objects.get_or_create(usuario=acudiente_user)

            Estudiante.objects.create(
                usuario=user,
                curso=curso,
                acudiente=acudiente_obj
            )
        
        elif rol == 'exalumno':
            año = form.cleaned_data.get('año_promoción')
            especialidad = form.cleaned_data.get('especialidad_tecnica')
            Exalumno.objects.create(
                usuario=user,
                año_promoción=año,
                especialidad_tecnica=especialidad
            )
        
        elif rol == 'acudiente':
            Acudiente.objects.create(usuario=user)
            
        # Añadimos la respuesta JSON para AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'full_name': user.get_full_name(),
                'rol': user.get_rol_display(), # Usamos get_rol_display para obtener el nombre legible
            })
            
        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)


class ListarUsuariosView(LoginRequiredMixin, ProfesorRequiredMixin, ListView):
    model = User
    template_name = "usuarios.html"
    context_object_name = "usuarios"

    # Pasamos el formulario de registro al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registro_form'] = UsuarioRegistroForm()
        return context


class EliminarUsuarioView(LoginRequiredMixin, ProfesorRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("usuarios")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Usuario eliminado correctamente.'})
        return redirect(self.get_success_url())
    

class CursoRegistroView(CreateView):
    model = Curso
    form_class = CursoRegistroForm
    template_name ="curso_registro.html"
    success_url = reverse_lazy("listar_cursos")

    # Override form_valid para responder con JSON si es una petición AJAX
    def form_valid(self, form):
        curso = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'id': curso.id,
                'nombre_curso': curso.nombre_curso,
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)


class EliminarCursoView(DeleteView):
    model = Curso
    success_url = reverse_lazy("listar_cursos")
    # Override post para responder con JSON si es una petición AJAX
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Curso eliminado correctamente.'})
        return redirect(self.get_success_url())

class ListarCursosView(LoginRequiredMixin, ProfesorRequiredMixin, ListView):
    model = Curso 
    template_name = "listar_cursos.html"
    context_object_name = "cursos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso_form'] = CursoRegistroForm()
        return context


class MateriaRegistroView(CreateView): 
    model = Materia
    form_class = MateriaRegistroForm
    template_name = "materias_registro.html"
    success_url = reverse_lazy("listar_materias")

    def form_valid(self, form):
        materia = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Devolvemos los datos de la nueva materia, incluyendo los nombres de las relaciones
            return JsonResponse({
                'id': materia.id,
                'nombre': materia.nombre,
                'curso_nombre': materia.curso.nombre_curso,
                'profesor_nombre': materia.profesor.usuario.get_full_name(),
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)


class ListarMateriasView(ListView):
    model = Materia 
    template_name = "listar_materias.html"
    context_object_name = "materias"

    # Pasamos el formulario de registro al contexto de la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materia_form'] = MateriaRegistroForm()
        return context


class EliminarMateriasView(DeleteView):
    model = Materia
    success_url = reverse_lazy("listar_materias")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Materia eliminada correctamente.'})
        return redirect(self.get_success_url())
    
    
class HorarioRegistroView(CreateView):
    model = Horario
    form_class = HorarioRegistroForm
    template_name = "registro_horario.html"
    success_url = reverse_lazy("listar_horarios")

    def form_valid(self, form):
        horario = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Devolvemos los datos, incluyendo el nombre de la materia
            return JsonResponse({
                'id': horario.id,
                'curso_nombre': horario.materia.curso.nombre_curso,
                'materia_nombre': horario.materia.nombre,
                'dia_semana': horario.dia_semana,
                # Formateamos la hora para mostrarla bien en JS
                'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
                'hora_fin': horario.hora_fin.strftime('%H:%M'),
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)


class ListarHorariosView(ListView):
    model = Horario
    template_name = "listar_horarios.html"
    context_object_name = "horarios"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['horario_form'] = HorarioRegistroForm()
        return context


class EliminarHorarioView(DeleteView):
    model = Horario
    success_url = reverse_lazy("listar_horarios")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Horario eliminado correctamente.'})
        return redirect(self.get_success_url())
    
    
class MiHorarioView(LoginRequiredMixin, EstudianteRequiredMixin, HorarioSemanalMixin, TemplateView):
    template_name = 'mi_horario.html'

    def get_horarios_base(self):
        try:
            estudiante = self.request.user.perfil_estudiante
            return Horario.objects.filter(materia__curso=estudiante.curso).order_by('hora_inicio')
        except User.perfil_estudiante.RelatedObjectDoesNotExist:
            return Horario.objects.none()
    
    def get_asistencias_semana(self, inicio, fin):
        try:
            estudiante = self.request.user.perfil_estudiante
            return Asistencia.objects.filter(estudiante=estudiante, fecha__range=[inicio, fin])
        except User.perfil_estudiante.RelatedObjectDoesNotExist:
            return Asistencia.objects.none()


class MiHorarioProfesorView(LoginRequiredMixin, ProfesorRequiredMixin, HorarioSemanalMixin, TemplateView):
    template_name = 'horario_profesor.html'

    def get_horarios_base(self):
        """
        Le dice al Mixin qué horarios base debe buscar para este profesor.
        """
        try:
            profesor = self.request.user.perfil_profesor
            return Horario.objects.filter(materia__profesor=profesor).order_by('hora_inicio')
        except User.perfil_profesor.RelatedObjectDoesNotExist:
            # Si el usuario no tiene perfil de profesor, no devuelve horarios.
            return Horario.objects.none()

    def get_asistencias_semana(self, inicio, fin):
        """
        Le dice al Mixin qué asistencias debe buscar para colorear el horario.
        """
        try:
            profesor = self.request.user.perfil_profesor
            return Asistencia.objects.filter(
                horario__materia__profesor=profesor,
                fecha__range=[inicio, fin]
            )
        except User.perfil_profesor.RelatedObjectDoesNotExist:
            return Asistencia.objects.none()


class TomarAsistenciaView(LoginRequiredMixin, ProfesorRequiredMixin, View):
    template_name = 'tomar_asistencia.html'

    # 'fecha' ahora viene de la URL
    def get(self, request, horario_id, fecha):
        horario = get_object_or_404(Horario, pk=horario_id)
        fecha_obj = date.fromisoformat(fecha) # Convertimos el texto de la URL a un objeto fecha
        
        curso = horario.materia.curso
        estudiantes = Estudiante.objects.filter(curso=curso).order_by('usuario__last_name')
        
        # Buscamos las asistencias para la fecha específica que nos pasaron
        asistencias_dia = Asistencia.objects.filter(horario=horario, fecha=fecha_obj)
        estados_guardados = {a.estudiante.pk: a.estado for a in asistencias_dia}

        context = {
            'horario': horario,
            'estudiantes': estudiantes,
            'estados_guardados': estados_guardados,
            'fecha': fecha_obj, # Pasamos la fecha a la plantilla para mostrarla
        }
        return render(request, self.template_name, context)

    def post(self, request, horario_id, fecha):
        horario = get_object_or_404(Horario, pk=horario_id)
        fecha_obj = date.fromisoformat(fecha)
        curso = horario.materia.curso
        estudiantes = Estudiante.objects.filter(curso=curso)

        for estudiante in estudiantes:
            estado_seleccionado = request.POST.get(f'asistencia-{estudiante.pk}')

            if estado_seleccionado:
                asistencia_obj, created = Asistencia.objects.update_or_create(
                    horario=horario,
                    estudiante=estudiante,
                    fecha=fecha_obj,
                    defaults={'estado': estado_seleccionado}
                )

                # --- LÓGICA DE ENVÍO DE CORREO ---
                # Si el estado es 'ausente' Y el estudiante tiene un acudiente con correo
                if estado_seleccionado == 'ausente' and estudiante.acudiente and estudiante.acudiente.usuario.email:
                    self.enviar_correo_ausencia(estudiante, horario, fecha_obj)

        messages.success(request, f'Asistencia para el {fecha_obj.strftime("%d/%m/%Y")} guardada correctamente.')
        return redirect(f"{reverse('horario_profesor')}?fecha={fecha}")

    def enviar_correo_ausencia(self, estudiante, horario, fecha):
        acudiente = estudiante.acudiente
        context = {
            'estudiante': estudiante,
            'horario': horario,
            'fecha': fecha,
        }
        
        subject = f"Notificación de Ausencia: {estudiante.usuario.get_full_name()}"
        html_message = render_to_string('notificacion_ausencia.html', context)
        plain_message = f"El estudiante {estudiante.usuario.get_full_name()} no asistió a la clase de {horario.materia.nombre} el {fecha}."
        
        send_mail(
            subject,
            plain_message,
            'noreply@tuinstitucion.com', # Remitente
            [acudiente.usuario.email],   # Destinatario
            html_message=html_message
        )


class HorariosAcudienteView(LoginRequiredMixin, AcudienteRequiredMixin, TemplateView):
    template_name = 'horarios_acudiente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenemos la fecha de la URL, o la de hoy si no existe
        fecha_str = self.request.GET.get('fecha')
        hoy = date.fromisoformat(fecha_str) if fecha_str else timezone.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())

        try:
            acudiente = self.request.user.perfil_acudiente
            estudiantes = acudiente.estudiantes_acudidos.all().select_related('usuario', 'curso')

            datos_horarios = []
            for estudiante in estudiantes:
                # Obtenemos los datos para este estudiante específico
                horarios_base = Horario.objects.filter(materia__curso=estudiante.curso)
                asistencias_semana = Asistencia.objects.filter(estudiante=estudiante, fecha__range=[inicio_semana, inicio_semana + timedelta(days=4)])
                
                # Usamos nuestra función de ayuda para construir el horario
                horario_semanal_estudiante = construir_horario_semanal(horarios_base, asistencias_semana, inicio_semana)

                datos_horarios.append({
                    'estudiante': estudiante,
                    'horario_semanal': horario_semanal_estudiante,
                })

            context['datos_horarios'] = datos_horarios
            # Añadimos las fechas de navegación al contexto principal
            context['semana_anterior'] = inicio_semana - timedelta(days=7)
            context['semana_siguiente'] = inicio_semana + timedelta(days=7)
            context['semana_actual_str'] = f"{inicio_semana.strftime('%d/%m/%Y')} - {(inicio_semana + timedelta(days=4)).strftime('%d/%m/%Y')}"
        
        except User.perfil_acudiente.RelatedObjectDoesNotExist:
            context['datos_horarios'] = []

        return context