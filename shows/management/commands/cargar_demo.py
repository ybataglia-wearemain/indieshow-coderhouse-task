from datetime import time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from shows.models import Genero, Show

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea géneros, usuarios y shows de demostración.'

    def handle(self, *args, **options):
        generos = {}
        for nombre in ['Indie Rock', 'Indie Pop', 'Rock Alternativo', 'Folk', 'Electrónica']:
            genero, _ = Genero.objects.get_or_create(nombre=nombre)
            generos[nombre] = genero

        admin, creado = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@indieshow.local', 'is_staff': True, 'is_superuser': True},
        )
        if creado:
            admin.set_password('Admin12345!')
            admin.save()
        elif not admin.is_superuser:
            admin.is_staff = True
            admin.is_superuser = True
            admin.save(update_fields=['is_staff', 'is_superuser'])

        bandas = [
            {
                'username': 'luzpolar',
                'password': 'Indie12345!',
                'email': 'luzpolar@indieshow.local',
                'nombre': 'Luz Polar',
                'genero': generos['Indie Rock'],
                'ciudad': 'Buenos Aires',
                'bio': 'Banda independiente de guitarras, sintetizadores y canciones nocturnas.',
            },
            {
                'username': 'domingorojo',
                'password': 'Indie12345!',
                'email': 'domingorojo@indieshow.local',
                'nombre': 'Domingo Rojo',
                'genero': generos['Rock Alternativo'],
                'ciudad': 'La Plata',
                'bio': 'Proyecto alternativo con canciones directas y energía en vivo.',
            },
        ]

        usuarios = {}
        for datos in bandas:
            usuario, creado = User.objects.get_or_create(
                username=datos['username'],
                defaults={'email': datos['email']},
            )
            if creado:
                usuario.set_password(datos['password'])
                usuario.save()
            perfil = usuario.perfil
            perfil.nombre_banda = datos['nombre']
            perfil.genero = datos['genero']
            perfil.ciudad = datos['ciudad']
            perfil.biografia = datos['bio']
            perfil.save()
            usuarios[datos['username']] = usuario

        hoy = timezone.localdate()
        shows_demo = [
            {
                'autor': usuarios['luzpolar'],
                'genero': generos['Indie Rock'],
                'titulo': 'Luz Polar en Club Horizonte',
                'fecha': hoy + timedelta(days=7),
                'hora': time(21, 0),
                'lugar': 'Club Horizonte',
                'direccion': 'Av. Corrientes 1500',
                'ciudad': 'Buenos Aires',
                'descripcion': 'Presentación en vivo del nuevo EP de Luz Polar con banda invitada y apertura de puertas a las 20 horas.',
                'precio': Decimal('12000.00'),
            },
            {
                'autor': usuarios['domingorojo'],
                'genero': generos['Rock Alternativo'],
                'titulo': 'Domingo Rojo presenta Sesiones',
                'fecha': hoy + timedelta(days=14),
                'hora': time(20, 30),
                'lugar': 'Sala Central',
                'direccion': 'Calle 48 620',
                'ciudad': 'La Plata',
                'descripcion': 'Show íntimo de Domingo Rojo con repertorio propio y versiones especiales preparadas para esta fecha.',
                'precio': Decimal('9000.00'),
            },
            {
                'autor': usuarios['luzpolar'],
                'genero': generos['Indie Pop'],
                'titulo': 'Festival IndieShow Vol. 1',
                'fecha': hoy + timedelta(days=28),
                'hora': time(18, 0),
                'lugar': 'Galpón Cultural Sur',
                'direccion': 'Defensa 900',
                'ciudad': 'Buenos Aires',
                'descripcion': 'Una tarde con proyectos independientes, feria de discos y cinco bandas en vivo en un mismo escenario.',
                'precio': None,
            },
        ]

        for datos in shows_demo:
            Show.objects.get_or_create(
                titulo=datos['titulo'],
                autor=datos['autor'],
                defaults=datos,
            )

        self.stdout.write(self.style.SUCCESS('Datos demo cargados correctamente.'))
        self.stdout.write('Admin: admin / Admin12345!')
        self.stdout.write('Banda: luzpolar / Indie12345!')
        self.stdout.write('Banda: domingorojo / Indie12345!')
