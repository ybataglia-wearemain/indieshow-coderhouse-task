from django.conf import settings
from django.db import models

from shows.models import Genero


class Perfil(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    nombre_banda = models.CharField(max_length=100, blank=True)
    genero = models.ForeignKey(
        Genero,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='perfiles',
    )
    ciudad = models.CharField(max_length=80, blank=True)
    biografia = models.TextField(blank=True)
    logo = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    instagram = models.URLField(blank=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.nombre_banda or self.usuario.username
