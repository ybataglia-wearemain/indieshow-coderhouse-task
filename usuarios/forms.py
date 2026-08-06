from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Perfil

User = get_user_model()


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre_banda = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'nombre_banda', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe un usuario con ese email.')
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
            perfil = usuario.perfil
            perfil.nombre_banda = self.cleaned_data['nombre_banda']
            perfil.save()
        return usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.usuario_actual = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        consulta = User.objects.filter(email__iexact=email)
        if self.usuario_actual:
            consulta = consulta.exclude(pk=self.usuario_actual.pk)
        if consulta.exists():
            raise forms.ValidationError('Ya existe un usuario con ese email.')
        return email


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre_banda', 'genero', 'ciudad', 'biografia', 'logo', 'instagram']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 5}),
        }
