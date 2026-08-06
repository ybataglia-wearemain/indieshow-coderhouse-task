from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegistroTests(TestCase):
    def test_registro_crea_usuario_y_perfil(self):
        respuesta = self.client.post(
            reverse('registro'),
            {
                'username': 'nuevabanda',
                'email': 'banda@example.com',
                'first_name': 'Ana',
                'last_name': 'Pérez',
                'nombre_banda': 'Nueva Banda',
                'password1': 'ClaveSegura123!',
                'password2': 'ClaveSegura123!',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        usuario = User.objects.get(username='nuevabanda')
        self.assertEqual(usuario.perfil.nombre_banda, 'Nueva Banda')

    def test_email_no_se_puede_repetir(self):
        User.objects.create_user(username='existente', email='repetido@example.com', password='Clave12345!')
        respuesta = self.client.post(
            reverse('registro'),
            {
                'username': 'otra',
                'email': 'repetido@example.com',
                'nombre_banda': 'Otra Banda',
                'password1': 'ClaveSegura123!',
                'password2': 'ClaveSegura123!',
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Ya existe un usuario con ese email.')
