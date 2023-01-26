from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from urna.models import Urna

def usuarios(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    usuario = request.user.get_username()
    return redirect('/%s' % usuario)

def gerente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    erro_inicio = 0
    msg_erro_inicio = ''
    if not ( urna.data_votacao is None and urna.hora_inicio is None and urna.hora_fim is None ):
        if (urna.data_votacao is not None) and (urna.hora_inicio is None and urna.hora_fim is None):
            erro_inicio = 1
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir os horários de início e de fim da votação !!!'
        elif (urna.data_votacao is not None) and (urna.hora_inicio is not None and urna.hora_fim is None):
            erro_inicio = 2
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir o horário de fim da votação !!!'
        elif (urna.data_votacao is not None) and (urna.hora_inicio is None and urna.hora_fim is not None):
            erro_inicio = 3
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir o horário de início da votação !!!'
        elif (urna.data_votacao is None) and (urna.hora_inicio is not None and urna.hora_fim is None):
            erro_inicio = 4
            msg_erro_inicio = 'ERRO: data não programada para votação !!!<br/>\
            Falta agora definir também o horário de fim da votação !!!'
        elif (urna.data_votacao is None) and (urna.hora_inicio is None and urna.hora_fim is not None):
            erro_inicio = 5
            msg_erro_inicio = 'ERRO: data não programada para votação !!!<br/>\
            Falta agora definir também o horário de início da votação !!!'
    return render(request, 'usuarios/gerente.html', {
        'erro_inicio': erro_inicio, 'msg_erro_inicio': msg_erro_inicio,
    })

def assistente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    erro = False
    msg_erro = ''
    if urna.data_votacao is None:
        erro = True
        msg_erro = 'ERRO: data não programada para votação !!!'
    elif urna.hora_inicio is None or urna.hora_fim is None:
        erro = True
        msg_erro = 'ERRO: horário não programado para votação !!!'
    elif not ( urna.hora_inicio <= datetime.now() and urna.hora_fim >= datetime.now() ):
        erro = True
        if urna.hora_inicio > datetime.now():
            msg_erro = 'ERRO: o horário de votação ainda não iniciou !!!'
        if urna.hora_fim < datetime.now():
            msg_erro = 'ERRO: o horário de votação já se encerrou !!!'
    return render(request, 'usuarios/assistente.html', {'erro': erro, 'msg_erro': msg_erro})
