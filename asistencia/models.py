from django.db import models

class Estudiante(models.Model):
    
    usuario_id = models.CharField(
        verbose_name='Usuario',
        max_length=150,
    )
    acudiente_id = models.CharField(
        verbose_name='Acudiente',
        max_length=150,
    )
    id_curso = models.PositiveSmallIntegerField(
        verbose_name='Curso',
    )


class Curso(models.Model) :
    
    nombre_curso=models.CharField(
        verbose_name='Nombre curso',
        max_length=150,
    )
    id_profesor = models.CharField(
        verbose_name='Profesor',
        max_length=100,
    )