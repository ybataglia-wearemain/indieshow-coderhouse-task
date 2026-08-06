from .models import Genero


def generos_menu(request):
    return {'generos_menu': Genero.objects.all()}
