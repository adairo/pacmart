from django import forms
from .models import Valoracion

class ValForm(forms.ModelForm):

    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']