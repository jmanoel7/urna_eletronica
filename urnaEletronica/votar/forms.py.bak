from django.conf import settings
from django import forms
from urna.models import dataVotacao


class formIniciarVotacao(forms.ModelForm):
    class Meta:
        model = dataVotacao
        fields = ('data_votacao', 'hora_inicio', 'hora_fim')

