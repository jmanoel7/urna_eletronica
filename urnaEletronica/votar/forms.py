from django.conf import settings
from django import forms
from urna.models import Urna


class formIniciarVotacao(forms.ModelForm):
    class Meta:
        model = Urna
        fields = ('data_votacao', 'hora_inicio', 'hora_fim')

