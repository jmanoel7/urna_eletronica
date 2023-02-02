from django.shortcuts import render
from urna.models import Urna, Politico, Eleitor, Voto, Resultado
from .forms import formIniciarVotacao
from datetime import datetime, time, timedelta

def iniciar_votacao(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
        urna_id = urna.id
        form = formIniciarVotacao()
        erro = False
        return render(request, 'votar/iniciar-votacao.html',
            {
                'form': form,
                'urna': urna,
                'urna_id': urna_id,
                'erro': erro,
            }
        )
    elif request.method == 'POST':
        erro = True
        form = formIniciarVotacao(request.POST)
        if form.is_valid():
            urna_id = request.POST.get('urna_id')
            if urna_id is None:
                urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
                urna_id = urna.id
            else:
                urna = Urna.objects.get(id=urna_id)
            data_votacao = request.POST.get('data_votacao')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fim = request.POST.get('hora_fim')
            if (data_votacao is None) or (hora_inicio is None) or (hora_fim is None):
                return render(request, 'votar/iniciar-votacao.html',
                    {
                        'form': form,
                        'urna': urna,
                        'urna_id': urna_id,
                        'erro': erro,
                    }
                )
            elif (len( data_votacao.__str__() ) == 0) or \
                (len( hora_inicio.__str__() ) == 0) or \
                (len( hora_fim.__str__() ) == 0):
                return render(request, 'votar/iniciar-votacao.html',
                    {
                        'form': form,
                        'urna': urna,
                        'urna_id': urna_id,
                        'erro': erro,
                    }
                )
            else:
                urna.data_votacao = data_votacao
                urna.hora_inicio = hora_inicio
                urna.hora_fim = hora_fim
                urna.save()
                return render(request, 'votar/iniciar-votacao-sucesso.html')
        else:
            urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
            urna_id = urna.id
            return render(request, 'votar/iniciar-votacao.html',
                {
                    'form': form,
                    'urna': urna,
                    'urna_id': urna_id,
                    'erro': erro,
                }
            )


def terminar_votacao(request):
    urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
    if (urna.data_votacao == datetime.now().date()) and (urna.hora_fim >= datetime.now().time()):
        cargo = 'Presidente da República'
        politico_branco = Politico.objects.get(
            politico='Branco', partido='BRANCO', num_partido='  ', cargo=cargo
        )
        politico_nulo = Politico.objects.get(
            politico='Nulo', partido='NULO', num_partido='00', cargo=cargo
        )
        politico_pt = Politico.objects.get(
            politico='Lula', partido='PT', num_partido='13', cargo=cargo
        )
        politico_pl = Politico.objects.get(
            politico='Bolsonaro', partido='PL', num_partido='22', cargo=cargo
        )
        votos_branco = politico_branco.votos.all()
        votos_nulo = politico_nulo.votos.all()
        votos_pt = politico_pt.votos.all()
        votos_pl = politico_pl.votos.all()
        votos_invalidos = votos_branco + votos_nulo
        votos_validos = votos_pt + votos_pl
        total_votos = urna.votos.all()
        total_eleitores = urna.eleitores.all()
        ausentes = total_eleitores - total_votos
        # voto_branco = Voto.objects.filter(politico_id=politico_branco.id)
        # voto_nulo = Voto.objects.filter(politico_id=politico_nulo.id)
        # voto_pt = Voto.objects.filter(politico_id=politico_pt.id)
        # voto_pl = Voto.objects.filter(politico_id=politico_pl.id)
        resultado = Resultado.objects.create(
            ausentes = ausentes,
            votos_nulo = votos_nulo,
            votos_branco = votos_branco,
            votos_invalidos = votos_invalidos,
            votos_candidato_A = votos_pl,
            votos_candidato_B = votos_pt,
            votos_validos = votos_validos,
            total_votos = total_votos,
        )
        resultado.save()
        return render(request, 'votar/terminar-votacao.html', {'erro': False, 'resultado': resultado})
    else:
        return render(request, 'votar/terminar-votacao.html', {'erro': True, 'resultado': None})


def eleitor(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0035', secao='0080', municipio='Goiânia', uf='GO')
        urna_id = urna.id
        eleitores = urna.eleitores.all()
        return render(request, 'votar/selecionar-eleitor.html',
            { 'eleitores': eleitores, 'eleitor': None, 'urna': urna, 'urna_id': urna_id, 'erro': False }
        )
    elif request.method == 'POST':
        urna = request.POST.get('urna')
        urna_id = request.POST.get('urna_id')
        eleitores = urna.eleitores.all()
        titulo_eleitor = request.POST.get('titulo_eleitor')
        eleitor_bd = Eleitor.objects.get(titulo_eleitor=titulo_eleitor)
        eleitor_id = eleitor_bd.id
        cargo = 'Presidente da República'
        voto_bd = Voto.objects.get(eleitor_id=eleitor_id, cargo=cargo)
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
                { 'eleitores': eleitores, 'eleitor': eleitor_bd, 'urna': urna, 'urna_id': urna_id, 'erro': True }
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
            voto = Voto.objects.create(
                eleitor_id=eleitor_id,
                politico_id=politico_id,
                urna_id=urna_id,
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

