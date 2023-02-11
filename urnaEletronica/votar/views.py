from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from urna.models import Urna, Politico, Eleitor, Voto, Resultado, dataVotacao
from .forms import formIniciarVotacao
from datetime import datetime

def iniciar_votacao(request):
    if request.method == 'GET':
        form = formIniciarVotacao()
        return render(request, 'votar/iniciar-votacao.html', {'form': form, 'erro': False})
    elif request.method == 'POST':
        form = formIniciarVotacao(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'votar/iniciar-votacao-sucesso.html')
        else:
            return render(request, 'votar/iniciar-votacao.html', {'form': form, 'erro': True})


def terminar_votacao(request):
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    try:
        data_obj = dataVotacao.objects.get(data_votacao=datetime.now().date())
    except ObjectDoesNotExist:
        data_obj= None
    if data_obj is not None:
        if data_obj.hora_inicio > datetime.now().time():
            return render(request, 'votar/terminar-votacao.html',
                {
                    'erro': True,
                    'msg_erro': 2,
                    'msg_voto': None,
                    'calculo': None,
                    'resultado': None,
                }
            )
        elif ( data_obj.hora_inicio <= datetime.now().time() ) and \
            ( data_obj.hora_fim >= datetime.now().time() ):
            return render(request, 'votar/terminar-votacao.html',
                {
                    'erro': True,
                    'msg_erro': 3,
                    'msg_voto': None,
                    'calculo': None,
                    'resultado': None,
                }
            )
        elif data_obj.hora_fim < datetime.now().time():
            cargo = 'Presidente da República'
            politico_branco = Politico.objects.get(
                politico='Branco', partido='BRANCO', num_partido='00', cargo=cargo
            )
            politico_nulo = Politico.objects.get(
                politico='Nulo', partido='NULO', num_partido='99', cargo=cargo
            )
            politico_pt = Politico.objects.get(
                politico='Lula', partido='PT', num_partido='13', cargo=cargo
            )
            politico_pl = Politico.objects.get(
                politico='Bolsonaro', partido='PL', num_partido='22', cargo=cargo
            )
            votos_branco = len(Voto.objects.filter(
                politico_id = politico_branco.id,
                data_votacao_id = data_obj.id,
            ))
            votos_nulo = len(Voto.objects.filter(
                politico_id = politico_nulo.id,
                data_votacao_id = data_obj.id,
            ))
            votos_pt = len(Voto.objects.filter(
                politico_id = politico_pt.id,
                data_votacao_id = data_obj.id,
            ))
            votos_pl = len(Voto.objects.filter(
                politico_id = politico_pl.id,
                data_votacao_id = data_obj.id,
            ))
            votos_invalidos = votos_branco + votos_nulo
            votos_validos = votos_pt + votos_pl
            total_votos = len(Voto.objects.filter(
                    urna_id = urna.id,
                    data_votacao_id = data_obj.id,
            ))
            total_eleitores = len( urna.eleitores.all() )
            ausentes = total_eleitores - total_votos
            resultado = Resultado.objects.create(
                ausentes = ausentes,
                votos_nulo = votos_nulo,
                votos_branco = votos_branco,
                votos_invalidos = votos_invalidos,
                votos_candidato_A = votos_pl,
                votos_candidato_B = votos_pt,
                votos_validos = votos_validos,
                total_votos = total_votos,
                total_eleitores = total_eleitores,
            )
            resultado.save()
            # votos inválidos
            if resultado.votos_invalidos == 0:
                voto_nulo = 0
                voto_branco = 0
            elif resultado.votos_invalidos > 0:
                voto_nulo = (resultado.votos_nulo / resultado.votos_invalidos) * 100
                voto_branco = (resultado.votos_branco / resultado.votos_invalidos) * 100
            # votos válidos
            if resultado.votos_validos == 0:
                voto_pt = 0
                voto_pl = 0
            elif resultado.votos_validos > 0:
                voto_pt = (resultado.votos_candidato_B / resultado.votos_validos) * 100
                voto_pl = (resultado.votos_candidato_A / resultado.votos_validos) * 100
            # total votos
            if resultado.total_votos == 0:
                votos_validos = 0
                votos_invalidos = 0
            elif resultado.total_votos > 0:
                votos_validos = (resultado.votos_validos / resultado.total_votos) * 100
                votos_invalidos = (resultado.votos_invalidos / resultado.total_votos) * 100
            total_votos = (resultado.total_votos / resultado.total_eleitores) * 100
            ausentes = (resultado.ausentes / resultado.total_eleitores) * 100
            # correcao dos votos para apresentacao na tabela final - inicio
            if voto_nulo == 0.0:
                voto_nulo = 0
            elif voto_nulo == 100.0:
                voto_nulo = 100
            if voto_branco == 0.0:
                voto_branco = 0
            elif voto_branco == 100.0:
                voto_branco = 100
            if voto_pl == 0.0:
                voto_pl = 0
            elif voto_pl == 100.0:
                voto_pl = 100
            if voto_pt == 0.0:
                voto_pt = 0
            elif voto_pt == 100.0:
                voto_pt = 100
            if votos_validos == 0.0:
                votos_validos = 0
            elif votos_validos == 100.0:
                votos_validos = 100
            if votos_invalidos == 0.0:
                votos_invalidos = 0
            elif votos_invalidos == 100.0:
                votos_invalidos = 100
            if total_votos == 0.0:
                total_votos = 0
            elif total_votos == 100.0:
                total_votos = 100
            if ausentes == 0.0:
                ausentes = 0
            elif ausentes == 100.0:
                ausentes = 100
            # correcao dos votos para apresentacao na tabela final - fim
            # verificacao do vencedor da eleicao - inicio
            if voto_pl == 0 and voto_pt == 0:
                msg_voto = 0
            elif voto_pt == voto_pl:
                msg_voto = 1
            elif voto_pl > voto_pt:
                msg_voto = 2
            elif voto_pt > voto_pl:
                msg_voto = 3
            # verificacao do vencedor da eleicao - fim
            calculo = {
                'voto_nulo': voto_nulo,
                'voto_branco': voto_branco,
                'voto_pl': voto_pl,
                'voto_pt': voto_pt,
                'votos_validos': votos_validos,
                'votos_invalidos': votos_invalidos,
                'total_votos': total_votos,
                'ausentes': ausentes,
            }
            return render(request, 'votar/terminar-votacao.html',
                {
                    'erro': False,
                    'msg_erro': 0,
                    'msg_voto': msg_voto,
                    'calculo': calculo,
                    'resultado': resultado,
                }
            )
    else:
        return render(request, 'votar/terminar-votacao.html',
            {
                'erro': True,
                'msg_erro': 1,
                'msg_voto': None,
                'calculo': None,
                'resultado': None,
            }
        )


def eleitor(request):
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    urna_id = urna.id
    eleitores = urna.eleitores.all()
    try:
        data_obj = dataVotacao.objects.get(data_votacao=datetime.now().date())
    except ObjectDoesNotExist:
        data_obj= None
    if data_obj is not None:
        if ( data_obj.hora_inicio <= datetime.now().time() ) and \
            ( data_obj.hora_fim >= datetime.now().time() ):
            pass
        else:
            if data_obj.hora_inicio > datetime.now().time():
                msg_erro = 1
            elif data_obj.hora_fim < datetime.now().time():
                msg_erro = 2
            return render(request, 'votar/selecionar-eleitor.html',
                {
                    'eleitores': eleitores,
                    'eleitor': None,
                    'urna': urna,
                    'urna_id': urna_id, 
                    'erro': True,
                    'msg_erro': msg_erro,
                }
            )
    else:
        return render(request, 'votar/selecionar-eleitor.html',
            {
                'eleitores': eleitores,
                'eleitor': None,
                'urna': urna,
                'urna_id': urna_id,
                'erro': True,
                'msg_erro': 3,
            }
        )
    if request.method == 'GET':
        return render(request, 'votar/selecionar-eleitor.html',
            {
                'eleitores': eleitores,
                'eleitor': None,
                'urna': urna,
                'urna_id': urna_id,
                'erro': False,
                'msg_erro': 0,
            }
        )
    elif request.method == 'POST':
        urna_id = request.POST.get('urna_id')
        urna = Urna.objects.get(id=urna_id)
        eleitores = urna.eleitores.all()
        titulo_eleitor = request.POST.get('titulo_eleitor')
        eleitor_bd = Eleitor.objects.get(titulo_eleitor=titulo_eleitor)
        eleitor_id = eleitor_bd.id
        cargo = 'Presidente da República'
        try:
            voto_bd = Voto.objects.get(eleitor_id=eleitor_id, cargo=cargo)
        except ObjectDoesNotExist:
            voto_bd = None
        if voto_bd is None:
            politicos = Politico.objects.filter(cargo=cargo)
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'erro': False,
                    'msg_erro': 0,
                }
            )
        else:
            return render(request, 'votar/selecionar-eleitor.html',
                {
                    'eleitores': eleitores,
                    'eleitor': eleitor_bd,
                    'urna': urna,
                    'urna_id': urna_id,
                    'erro': True,
                    'msg_erro': 4,
                }
            )
            

def votar(request):
    if request.method == 'GET':
        titulo_eleitor = request.GET.get('titulo_eleitor')
        urna_id = request.GET.get('urna_id')
        cargo = 'Presidente da República'
        politicos = Politico.objects.filter(cargo=cargo)
        return render(request, 'votar/urna.html',
            {
                'titulo_eleitor': titulo_eleitor,
                'urna_id': urna_id,
                'cargo': cargo,
                'politicos': politicos,
                'erro': False,
                'msg_erro': 0,
            }
        )
    elif request.method == 'POST':
        titulo_eleitor = request.POST.get('titulo_eleitor')
        urna_id = request.POST.get('urna_id')
        cargo = request.POST.get('cargo')
        politicos = request.POST.get('politicos')
        politico = request.POST.get('politico')
        partido = request.POST.get('partido')
        num_partido = request.POST.get('num_partido')
        if politico is None or partido is None:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'erro': True,
                    'msg_erro': 1,
                }
            )
        elif len(politico) == 0 or len(partido) == 0:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'erro': True,
                    'msg_erro': 2,
                }
            )
        elif ( politico == 'Branco' and partido != 'BRANCO' ) or \
             ( politico != 'Branco' and partido == 'BRANCO' ):
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'erro': True,
                    'msg_erro': 3,
                }
            )
        elif ( politico == 'Nulo' and partido != 'NULO' ) or \
             ( politico != 'Nulo' and partido == 'NULO' ):
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'erro': True,
                    'msg_erro': 4,
                }
            )
        elif ( politico == 'Branco' and partido == 'BRANCO' ) or \
             ( politico == 'Nulo' and partido == 'NULO' ) or \
             ( ( politico != 'Branco' and partido != 'BRANCO' ) and \
               ( politico != 'Nulo' and partido != 'NULO' ) ):
            politico_bd = Politico.objects.get(
                politico=politico,
                partido=partido,
                num_partido=num_partido,
                cargo=cargo,
                urna_id=urna_id,
            )
            politico_id = politico_bd.id
            eleitor_bd = Eleitor.objects.get(titulo_eleitor=titulo_eleitor)
            eleitor_id = eleitor_bd.id
            data_votacao_bd = dataVotacao.objects.get(data_votacao=datetime.now().date())
            data_votacao_id = data_votacao_bd.id
            voto = Voto.objects.create(
                eleitor_id=eleitor_id,
                politico_id=politico_id,
                urna_id=urna_id,
                data_votacao_id=data_votacao_id,
                cargo=cargo,
            )
            voto.save()
            return render(request, 'votar/registrar-voto.html',
                {
                    'num_partido_1': politico_bd.num_partido[0],
                    'num_partido_2': politico_bd.num_partido[1],
                    'politico': politico_bd.politico,
                    'partido': politico_bd.partido,
                    'cargo': politico_bd.cargo,
                    'foto': politico_bd.foto,
                }
            )
        else:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'erro': True,
                    'msg_erro': 5,
                }
            )
    else:
        return render(request, 'votar/urna.html',
            {
                'titulo_eleitor': titulo_eleitor,
                'urna_id': urna_id,
                'cargo': cargo,
                'politicos': politicos,
                'politico': politico,
                'partido': partido,
                'num_partido': num_partido,
                'erro': True,
                'msg_erro': 6,
            }
        )

