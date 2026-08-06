from django.contrib import admin, messages

from .models import Genero, Show


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'fecha', 'hora', 'ciudad', 'publicado')
    list_filter = ('publicado', 'genero', 'fecha', 'ciudad')
    search_fields = ('titulo', 'autor__username', 'autor__perfil__nombre_banda', 'lugar', 'ciudad')
    list_select_related = ('autor', 'genero')
    date_hierarchy = 'fecha'
    actions = ('publicar_shows', 'ocultar_shows')

    @admin.action(description='Publicar shows seleccionados')
    def publicar_shows(self, request, queryset):
        cantidad = queryset.filter(publicado=False).update(publicado=True)
        self.message_user(request, f'{cantidad} shows publicados.', messages.SUCCESS)

    @admin.action(description='Ocultar shows seleccionados')
    def ocultar_shows(self, request, queryset):
        cantidad = queryset.filter(publicado=True).update(publicado=False)
        self.message_user(request, f'{cantidad} shows ocultados.', messages.SUCCESS)
