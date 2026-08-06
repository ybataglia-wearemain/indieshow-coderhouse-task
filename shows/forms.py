from django import forms

from .models import Show


class BusquedaShowForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={'placeholder': 'Banda, show, ciudad o lugar'}),
    )


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            'titulo',
            'genero',
            'fecha',
            'hora',
            'lugar',
            'direccion',
            'ciudad',
            'descripcion',
            'flyer',
            'precio',
            'enlace_entradas',
            'publicado',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'descripcion': forms.Textarea(attrs={'rows': 6}),
            'precio': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo'].strip()
        if len(titulo) < 4:
            raise forms.ValidationError('El título debe tener al menos 4 caracteres.')
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion'].strip()
        if len(descripcion) < 20:
            raise forms.ValidationError('La descripción debe tener al menos 20 caracteres.')
        return descripcion
