from django import template

register = template.Library()


@register.filter
def precio_show(valor):
    if valor is None:
        return 'Entrada gratuita o precio a confirmar'
    return f'${valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


@register.simple_tag
def saludo_banda(user):
    if not user.is_authenticated:
        return 'Descubrí tu próximo show indie'
    nombre = getattr(user.perfil, 'nombre_banda', '') or user.username
    return f'Hola, {nombre}'
