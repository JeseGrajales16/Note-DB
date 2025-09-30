from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    # --- CAMPOS ADICIONALES PARA CADA ROL ---
    # Campos para Estudiante
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        label="Curso",
        required=False, # No es obligatorio para todos los roles
        widget=forms.Select(attrs={"class": "form-control"})
    )
    acudiente = forms.ModelChoiceField(
        queryset=User.objects.filter(rol='acudiente'), # Solo usuarios que son acudientes
        label="Acudiente",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Campos para Exalumno
    año_promoción = forms.CharField(
        max_length=4,
        label="Año de Promoción",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    especialidad_tecnica = forms.CharField(
        max_length=50,
        label="Especialidad Técnica",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "documento", "telefono", "email", "rol", 
            "password", "curso", "acudiente", "año_promoción", "especialidad_tecnica"
        ]
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
            "rol": forms.Select(attrs={"class": "form-control", "id": "id_rol"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')

        if rol == 'estudiante':
            if not cleaned_data.get('curso'):
                self.add_error('curso', 'Para el rol de estudiante, el curso es obligatorio.')
            if not cleaned_data.get('acudiente'):
                self.add_error('acudiente', 'Para el rol de estudiante, el acudiente es obligatorio.')
        
        elif rol == 'exalumno':
            if not cleaned_data.get('año_promoción'):
                self.add_error('año_promoción', 'Para el rol de exalumno, el año de promoción es obligatorio.')
            if not cleaned_data.get('especialidad_tecnica'):
                self.add_error('especialidad_tecnica', 'Para el rol de exalumno, la especialidad es obligatoria.')

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Usuario"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña"
        })
    )


class CursoRegistroForm(forms.ModelForm):
    
    class Meta:
        model = Curso
        fields = ["nombre_curso"]


class MateriaRegistroForm(forms.ModelForm):

    class Meta:
        model = Materia
        fields = ["nombre", "curso", "profesor"]


class AsistenciaRegistroForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['fecha', 'horario', 'estudiante', 'estado', 'observaciones']
        
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HorarioRegistroForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['materia', 'dia_semana', 'hora_inicio', 'hora_fin']
        
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin':    forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'materia':     forms.Select(attrs={'class': 'form-control'}),
            'dia_semana':  forms.Select(attrs={'class': 'form-control'}),
        }
