from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profesor, Estudiante, Acudiente

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.rol == "profesor":
            Profesor.objects.create(usuario=instance)
        elif instance.rol == "estudiante":
            Estudiante.objects.create(usuario=instance)
        elif instance.rol == "acudiente":
            Acudiente.objects.create(usuario=instance)