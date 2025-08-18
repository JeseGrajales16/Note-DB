from django import forms
from .models import User, Curso, Materia, Asistencia

class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [ "first_name", "last_name", "telefono","email", "rol", "documento", "password"]

class CursoRegistroForm(forms.ModelForm):
    
    class Meta:
        model = Curso
        fields = ["nombre_curso"]

class MateriaRegistroForm(forms.ModelForm):

    class Meta:
        model = Materia
        fields = ["nombre", "curso", "profesor"]

class AsistanciaRegistroFrom(forms.ModelForm):

    class Meta:
        model = Asistencia
        fields = ["nombre_asistencia"]
