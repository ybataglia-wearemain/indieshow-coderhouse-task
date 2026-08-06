from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_banda', models.CharField(blank=True, max_length=100)),
                ('ciudad', models.CharField(blank=True, max_length=80)),
                ('biografia', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='perfiles/')),
                ('instagram', models.URLField(blank=True)),
                ('genero', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfiles', to='shows.genero')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
    ]
