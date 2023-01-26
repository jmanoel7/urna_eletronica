from django.shortcuts import render, HttpResponse
from urna.models import Urna, Politico, Eleitor, Voto


def eleitor(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0135', secao='0080', municipio='Goiânia', uf='GO')
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

