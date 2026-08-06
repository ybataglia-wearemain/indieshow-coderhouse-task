from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=70, unique=True)),
            ],
            options={
                'verbose_name': 'género',
                'verbose_name_plural': 'géneros',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('lugar', models.CharField(max_length=120)),
                ('direccion', models.CharField(max_length=160)),
                ('ciudad', models.CharField(max_length=80)),
                ('descripcion', models.TextField()),
                ('flyer', models.ImageField(blank=True, null=True, upload_to='flyers/')),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('enlace_entradas', models.URLField(blank=True)),
                ('publicado', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to=settings.AUTH_USER_MODEL)),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shows', to='shows.genero')),
            ],
            options={
                'verbose_name': 'show',
                'verbose_name_plural': 'shows',
                'ordering': ['fecha', 'hora'],
            },
        ),
    ]
