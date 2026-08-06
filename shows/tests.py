from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Genero, Show

User = get_user_model()


class ShowTests(TestCase):
    def setUp(self):
        self.genero = Genero.objects.create(nombre='Indie Rock')
        self.usuario = User.objects.create_user(username='banda1', password='Clave12345!')
        self.otro_usuario = User.objects.create_user(username='banda2', password='Clave12345!')
        self.usuario.perfil.nombre_banda = 'Banda Uno'
        self.usuario.perfil.genero = self.genero
        self.usuario.perfil.save()
        self.show = Show.objects.create(
            autor=self.usuario,
            genero=self.genero,
            titulo='Fecha de prueba',
            fecha=timezone.localdate() + timedelta(days=5),
            hora=time(21, 0),
            lugar='Club de prueba',
            direccion='Calle 123',
            ciudad='Buenos Aires',
            descripcion='Descripción suficientemente larga para validar correctamente el formulario.',
            publicado=True,
        )

    def test_lista_publica_muestra_show(self):
        respuesta = self.client.get(reverse('lista_shows'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Fecha de prueba')

    def test_filtro_por_genero(self):
        respuesta = self.client.get(reverse('shows_por_genero', args=[self.genero.slug]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Fecha de prueba')

    def test_busqueda_por_ciudad(self):
        respuesta = self.client.get(reverse('lista_shows'), {'q': 'Buenos Aires'})
        self.assertContains(respuesta, 'Fecha de prueba')

    def test_crear_show_requiere_login(self):
        respuesta = self.client.get(reverse('crear_show'))
        self.assertEqual(respuesta.status_code, 302)

    def test_otro_usuario_no_puede_editar(self):
        self.client.login(username='banda2', password='Clave12345!')
        respuesta = self.client.get(reverse('editar_show', args=[self.show.pk]))
        self.assertEqual(respuesta.status_code, 404)

    def test_autor_puede_editar(self):
        self.client.login(username='banda1', password='Clave12345!')
        respuesta = self.client.get(reverse('editar_show', args=[self.show.pk]))
        self.assertEqual(respuesta.status_code, 200)
