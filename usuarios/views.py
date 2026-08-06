from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm, UsuarioForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            messages.success(request, 'Tu cuenta fue creada correctamente.')
            return redirect('editar_perfil')
    else:
        formulario = RegistroForm()

    return render(request, 'usuarios/registro.html', {'formulario': formulario})


@login_required
def perfil(request):
    shows = request.user.shows.select_related('genero').order_by('fecha', 'hora')
    return render(request, 'usuarios/perfil.html', {'shows': shows})


@login_required
@transaction.atomic
def editar_perfil(request):
    if request.method == 'POST':
        formulario_usuario = UsuarioForm(request.POST, instance=request.user)
        formulario_perfil = PerfilForm(
            request.POST,
            request.FILES,
            instance=request.user.perfil,
        )
        if formulario_usuario.is_valid() and formulario_perfil.is_valid():
            formulario_usuario.save()
            formulario_perfil.save()
            messages.success(request, 'Tu perfil fue actualizado.')
            return redirect('perfil')
    else:
        formulario_usuario = UsuarioForm(instance=request.user)
        formulario_perfil = PerfilForm(instance=request.user.perfil)

    return render(
        request,
        'usuarios/editar_perfil.html',
        {
            'formulario_usuario': formulario_usuario,
            'formulario_perfil': formulario_perfil,
        },
    )
