from django.conf import settings
from django import forms
from urna.models import dataVotacao


class formIniciarVotacao(forms.ModelForm):

    data_votacao = forms.DateField(
        label='Data da Votação',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            },
        ),
        input_formats=settings.DATE_INPUT_FORMATS,
    )

    hora_inicio = forms.TimeField(
        label='Hora do Início da Votação',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'type': 'time',
            },
        ),
        input_formats=('%H:%M',),
    )

    hora_fim = forms.TimeField(
        label='Hora do Fim da Votação',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'type': 'time',
            },
        ),
        input_formats=('%H:%M',),
    )

    class Meta:
        model = dataVotacao
        fields = ('data_votacao', 'hora_inicio', 'hora_fim', 'urna')
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['data_votacao'].widget.attrs.update(placeholder='YYYY-MM-DD')
    #     self.fields['hora_inicio'].widget.attrs.update(placeholder='HH:MM:SS')
    #     self.fields['hora_fim'].widget.attrs.update(placeholder='HH:MM:SS')

