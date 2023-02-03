from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from urna.models import Urna

def usuarios(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        usuario = request.user.get_username()
        return redirect('/%s' % usuario)

def gerente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return render(request, 'usuarios/gerente.html')
    '''
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    erro_inicio = False
    msg_erro_inicio = ''
    if not ( (urna.data_votacao is None) and (urna.hora_inicio is None) and (urna.hora_fim is None) ):
        erro_inicio = True
        if (urna.data_votacao is not None) and (urna.hora_inicio is None) and (urna.hora_fim is None):
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir os horários de início e de fim da votação !!!'
        elif (urna.data_votacao is not None) and (urna.hora_inicio is not None) and (urna.hora_fim is None):
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir o horário de fim da votação !!!'
        elif (urna.data_votacao is not None) and (urna.hora_inicio is None) and (urna.hora_fim is not None):
            msg_erro_inicio = 'ERRO: data já programada para votação !!!<br/>\
            Falta agora definir o horário de início da votação !!!'
        elif (urna.data_votacao is None) and (urna.hora_inicio is not None) and (urna.hora_fim is None):
            msg_erro_inicio = 'ERRO: data não programada para votação !!!<br/>\
            Falta agora definir também o horário de fim da votação !!!'
        elif (urna.data_votacao is None) and (urna.hora_inicio is None) and (urna.hora_fim is not None):
            msg_erro_inicio = 'ERRO: data não programada para votação !!!<br/>\
            Falta agora definir também o horário de início da votação !!!'
    erro_fim = False
    msg_erro_fim = ''
    if (urna.data_votacao is not None) and (urna.hora_inicio is not None) and (urna.hora_fim is not None):
        if urna.data_votacao > datetime.now().date():
            erro_fim = True
            msg_erro_fim = 'ERRO: data de votação futura !!!<br/>\
            Espere pela data ou redefina-a no botão <Iniciar Votação> !!!'
        elif urna.data_votacao < datetime.now().date():
            erro_fim = True
            msg_erro_fim = 'ERRO: data de votação passada !!!<br/>\
            Verifique se já ocorreu uma votação, ou<br/>\
            redefina-a clicando no botão <Iniciar Votação> !!!'
        elif urna.hora_inicio >= urna.hora_fim:
            erro_fim = True
            msg_erro_fim = 'ERRO: hora de início maior/igual que a hora de fim !!!<br/>\
            Corrija a votação clicando no botão <Iniciar Votação> !!!'
        elif urna.hora_fim > datetime.now().time():
            erro_fim = True
            msg_erro_fim = 'ERRO: não se pode encerrar essa votação por enquanto !!!<br/>\
            Espere pelo encerramento da votação às %s ou<br\>\
            redefina-a no botão <Iniciar Votação> !!!' % urna.hora_fim.__str__
    return render(request, 'usuarios/gerente.html', {
        'erro_inicio': erro_inicio, 'msg_erro_inicio': msg_erro_inicio,
        'erro_fim': erro_fim, 'msg_erro_fim': msg_erro_fim,
    })
    '''

def assistente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return render(request, 'usuarios/assistente.html')
    '''
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    erro = False
    msg_erro = None
    if urna.datas.data_votacao is None:
        erro = True
        msg_erro = 'ERRO: data não programada para votação !!!'
    elif urna.datas.hora_inicio is None:
        erro = True
        msg_erro = 'ERRO: horário de início não programado para votação !!!'
    elif urna.datas.hora_fim is None:
        erro = True
        msg_erro = 'ERRO: horário de fim não programado para votação !!!'
    elif not ( urna.hora_inicio <= datetime.now().time() and urna.hora_fim >= datetime.now().time() ):
        erro = True
        if urna.hora_inicio > datetime.now().time():
            msg_erro = 'ERRO: o horário de votação ainda não iniciou !!!'
        if urna.hora_fim < datetime.now().time():
            msg_erro = 'ERRO: o horário de votação já se encerrou !!!'
    return render(request, 'usuarios/assistente.html', {'erro': erro, 'msg_erro': msg_erro})
    '''