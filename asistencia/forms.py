from django import forms
from .models import User, Curso, Materia, Asistencia, Horario

class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "telefono", "email", "rol", "documento", "password"]
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "telefono": "Teléfono",
            "email": "Correo electrónico",
            "rol": "Rol",
            "documento": "Documento",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rol": forms.Select(attrs={"class": "form-control"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
        }


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
        fields = [ "estudiante", "profesor", "curso", "materia", "horario", "estado"]


class HorarioRegistroForm(forms.ModelForm):

    class Meta:
        model = Horario 
        # fields = [ "materia", "dia_semana", "hora_inicio", "hora_fin"] 
        fields = '__all__'
