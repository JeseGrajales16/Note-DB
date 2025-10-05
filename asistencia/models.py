from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError

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
        ('acudiente', 'Acudiente'),
        ('exalumno', 'Exalumno'),
    ]

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    first_name = models.CharField(max_length=150, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")
    telefono = models.CharField(max_length=100, verbose_name="Teléfono")
    rol = models.CharField(max_length=15, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de usuario")
    documento = models.CharField(max_length=30, verbose_name="Documento de identidad")

    is_staff = models.BooleanField(default=False, verbose_name="Es administrador")
    is_active = models.BooleanField(default=True, verbose_name="Está activo")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Fecha de registro")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'rol']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email
    

class Acudiente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_acudiente')

    def __str__(self):
        return self.usuario.get_full_name()


class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_profesor')

    def __str__(self):
        return self.usuario.get_full_name()


class Curso(models.Model):
    nombre_curso = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre_curso


class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_estudiante')
    acudiente = models.ForeignKey(Acudiente, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes_acudidos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes')

    def __str__(self):
        return self.usuario.get_full_name()
    

class Exalumno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_exalumno')
    año_promoción = models.CharField(max_length=4)
    especialidad_tecnica = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.get_full_name()
    

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materias')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='materias_dictadas')

    def __str__(self):
        return f"{self.nombre} ({self.curso.nombre_curso})"


class Horario(models.Model):
    DIA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=15, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.materia.nombre} - {self.dia_semana}"

    def clean(self):
        super().clean() # Llama a la validación por defecto primero
        
        # Si alguno de los campos necesarios no está presente, no podemos validar
        if not all([self.dia_semana, self.materia, self.hora_inicio, self.hora_fin]):
            return

        profesor = self.materia.profesor
        curso = self.materia.curso

        # 1. Verificación de Conflicto de Profesor
        conflicto_profesor = Horario.objects.filter(
            dia_semana=self.dia_semana,
            materia__profesor=profesor,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        ).exclude(pk=self.pk)

        if conflicto_profesor.exists():
            # Obtenemos el horario en conflicto para dar un mensaje más claro
            conflicto = conflicto_profesor.first()
            raise ValidationError(
                f'Conflicto de horario: El profesor {profesor} ya dicta "{conflicto.materia.nombre}" en el curso {conflicto.materia.curso} a esa hora.'
            )

        # 2. Verificación de Conflicto de Curso
        conflicto_curso = Horario.objects.filter(
            dia_semana=self.dia_semana,
            materia__curso=curso,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        ).exclude(pk=self.pk)

        if conflicto_curso.exists():
            conflicto = conflicto_curso.first()
            raise ValidationError(
                f'Conflicto de horario: El curso {curso} ya tiene la materia "{conflicto.materia.nombre}" asignada a esa hora.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Asistencia(models.Model):
    fecha = models.DateField(default=timezone.now) 
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='asistencias')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    estado = models.CharField(max_length=20, choices=[
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tarde', 'Tarde'),
        ('excusa', 'Excusa')
    ])
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('fecha', 'horario', 'estudiante')

    def __str__(self):
        return f"{self.estudiante} - {self.horario.materia.nombre} - {self.fecha}"
