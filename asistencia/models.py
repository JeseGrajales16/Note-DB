from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('acudiente', 'Acudiente')
    ]

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    first_name = models.CharField(max_length=150, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")
    telefono = models.CharField(max_length=100,  verbose_name="Número de Teléfono")
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de usuario")

    is_staff = models.BooleanField(default=False, verbose_name="Es administrador")
    is_active = models.BooleanField(default=True, verbose_name="Está activo")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Fecha de registro")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email


class Profesor(models.Model):
    usuario = models.OneToOneField(User, verbose_name="USuario",  max_length=100 )

    def __str__(self):
        return self.usuario.first_name


class Curso(models.Model) :   
    nombre_curso=models.CharField(verbose_name='Nombre curso', max_length=150, )
    profesor = models.ForeignKey(Profesor, verbose_name="profesor", max_length=100)

    def __str__(self):
        return self.nombre_curso

class Estudiante(models.Model):
    
    usuario = models.OneToOneField(User, verbose_name="USuario",  max_length=100 )
    acudiente = models.CharField( verbose_name='Acudiente', max_length=150, )
    curso = models.PositiveSmallIntegerField( verbose_name='Curso', )
    def __str__(self):
        return self.usuario.first_name


class Materia(models.Model):
    nombre = models.CharField( verbose_name="Nombre", max_length=100, )
    curso = models.CharField( verbose_name="Curso", max_length=10)
    profesor = models.CharField(verbose_name="Profesor", max_length=100,)
      
class Horario(models.Model):
    materia = models.ForeignKey(
        Materia,verbose_name="Materia", max_length=150,)
    dia_semana = models.CharField(verbose_name="Dia y Semana", max_length=150,)
    hora_inicio = models.CharField(verbose_name="Hora de inicio", max_length=100,)
    hora_fin = models.CharField(verbose_name="Hora final", max_length=100,)

class Asistencia(models.Model):
    estudiante = models.CharField(verbose_name= "Estudiante", max_length=150,)
    curso = models.CharField(verbose_name = "Curso", max_length=100,)
    profesor = models.CharField(verbose_name="Profesor", max_length=150,)
    materia = models.CharField(verbose_name="Materia")
    estado = models.CharField(verbose_name="Estado", max_length=150,)
