from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_banda', 'genero', 'ciudad')
    list_filter = ('genero', 'ciudad')
    search_fields = ('usuario__username', 'usuario__email', 'nombre_banda')
    list_select_related = ('usuario', 'genero')
