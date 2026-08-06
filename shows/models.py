from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Genero(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'género'
        verbose_name_plural = 'géneros'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Show(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shows',
    )
    genero = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        related_name='shows',
    )
    titulo = models.CharField(max_length=120)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=120)
    direccion = models.CharField(max_length=160)
    ciudad = models.CharField(max_length=80)
    descripcion = models.TextField()
    flyer = models.ImageField(upload_to='flyers/', blank=True, null=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    enlace_entradas = models.URLField(blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name = 'show'
        verbose_name_plural = 'shows'

    def clean(self):
        errores = {}
        if self.fecha and self.fecha < timezone.localdate():
            errores['fecha'] = 'La fecha del show no puede estar en el pasado.'
        if self.precio is not None and self.precio < Decimal('0'):
            errores['precio'] = 'El precio no puede ser negativo.'
        if errores:
            raise ValidationError(errores)

    def get_absolute_url(self):
        return reverse('detalle_show', args=[self.pk])

    @property
    def nombre_banda(self):
        perfil = getattr(self.autor, 'perfil', None)
        if perfil and perfil.nombre_banda:
            return perfil.nombre_banda
        return self.autor.username

    def __str__(self):
        return f'{self.titulo} - {self.nombre_banda}'
