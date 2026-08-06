from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('shows/', views.lista_shows, name='lista_shows'),
    path('shows/mios/', views.mis_shows, name='mis_shows'),
    path('shows/nuevo/', views.crear_show, name='crear_show'),
    path('shows/<int:pk>/', views.detalle_show, name='detalle_show'),
    path('shows/<int:pk>/editar/', views.editar_show, name='editar_show'),
    path('shows/<int:pk>/eliminar/', views.eliminar_show, name='eliminar_show'),
    path('genero/<slug:slug>/', views.shows_por_genero, name='shows_por_genero'),
]
