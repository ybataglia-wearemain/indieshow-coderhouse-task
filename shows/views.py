from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BusquedaShowForm, ShowForm
from .models import Genero, Show


def inicio(request):
    shows = (
        Show.objects.select_related('autor', 'autor__perfil', 'genero')
        .filter(publicado=True, fecha__gte=timezone.localdate())
        .order_by('fecha', 'hora')[:6]
    )
    return render(request, 'shows/inicio.html', {'shows': shows})


def lista_shows(request):
    formulario = BusquedaShowForm(request.GET or None)
    shows = (
        Show.objects.select_related('autor', 'autor__perfil', 'genero')
        .filter(publicado=True, fecha__gte=timezone.localdate())
    )
    query = ''

    if formulario.is_valid():
        query = formulario.cleaned_data.get('q', '')
        if query:
            shows = shows.filter(
                Q(titulo__icontains=query)
                | Q(autor__perfil__nombre_banda__icontains=query)
                | Q(ciudad__icontains=query)
                | Q(lugar__icontains=query)
            )

    return render(
        request,
        'shows/lista_shows.html',
        {'shows': shows, 'formulario': formulario, 'query': query},
    )


def shows_por_genero(request, slug):
    genero = get_object_or_404(Genero, slug=slug)
    shows = (
        Show.objects.select_related('autor', 'autor__perfil', 'genero')
        .filter(
            genero=genero,
            publicado=True,
            fecha__gte=timezone.localdate(),
        )
        .order_by('fecha', 'hora')
    )
    return render(
        request,
        'shows/shows_por_genero.html',
        {'genero': genero, 'shows': shows},
    )


def detalle_show(request, pk):
    show = get_object_or_404(
        Show.objects.select_related('autor', 'autor__perfil', 'genero'),
        pk=pk,
    )
    if not show.publicado and request.user != show.autor:
        raise PermissionDenied('Este show no está publicado.')
    return render(request, 'shows/detalle_show.html', {'show': show})


@login_required
def mis_shows(request):
    shows = (
        Show.objects.select_related('genero')
        .filter(autor=request.user)
        .order_by('fecha', 'hora')
    )
    return render(request, 'shows/mis_shows.html', {'shows': shows})


@login_required
def crear_show(request):
    if request.method == 'POST':
        formulario = ShowForm(request.POST, request.FILES)
        if formulario.is_valid():
            show = formulario.save(commit=False)
            show.autor = request.user
            show.save()
            messages.success(request, 'El show fue creado correctamente.')
            return redirect(show)
    else:
        inicial = {}
        if request.user.perfil.genero:
            inicial['genero'] = request.user.perfil.genero
        formulario = ShowForm(initial=inicial)

    return render(
        request,
        'shows/form_show.html',
        {'formulario': formulario, 'titulo_pagina': 'Publicar show'},
    )


@login_required
def editar_show(request, pk):
    show = get_object_or_404(Show, pk=pk, autor=request.user)

    if request.method == 'POST':
        formulario = ShowForm(request.POST, request.FILES, instance=show)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'El show fue actualizado correctamente.')
            return redirect(show)
    else:
        formulario = ShowForm(instance=show)

    return render(
        request,
        'shows/form_show.html',
        {'formulario': formulario, 'titulo_pagina': 'Editar show', 'show': show},
    )


@login_required
def eliminar_show(request, pk):
    show = get_object_or_404(Show, pk=pk, autor=request.user)

    if request.method == 'POST':
        show.delete()
        messages.success(request, 'El show fue eliminado.')
        return redirect('mis_shows')

    return render(request, 'shows/eliminar_show.html', {'show': show})
