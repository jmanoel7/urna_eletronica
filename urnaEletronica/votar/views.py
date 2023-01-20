from django.shortcuts import render, HttpResponse
from urna.models import Urna, Politico, Eleitor, Voto

def eleitor(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0135', secao='0080', municipio='Goiânia', uf='GO')
        urna_id = urna.id
        eleitores = urna.eleitores.all()
        return render(request, 'votar/selecionar-eleitor.html',
            { 'eleitores': eleitores, 'urna': urna, 'urna_id': urna_id }
        )

def votar(request):
    if request.method == 'GET':
        voto = request.GET.get('voto')
        if voto:
            titulo_eleitor = request.GET.get('titulo_eleitor')
            urna_id = request.GET.get('urna_id')
            cargo = 'Presidente da República'
            politicos = Politico.objects.filter(cargo=cargo)
            # print("titulo_eleitor: %s" % titulo_eleitor)
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna_id': urna_id,
                    'cargo': cargo,
                    'politicos': politicos,
                    'erro': False
                }
            )
        abstencao = request.GET.get('abstencao')
        if abstencao:
            return HttpResponse('<h1>%s</h1>' % abstencao)
    elif request.method == 'POST':
        titulo_eleitor = request.POST.get('titulo_eleitor')
        urna_id = request.POST.get('urna_id')
        cargo = request.POST.get('cargo')
        politicos = request.POST.get('politicos')
        politico = request.POST.get('politico')
        partido = request.POST.get('partido')
        num_partido = request.POST.get('num_partido')
        # print('partido: %s' % partido)
        # print('titulo_eleitor: %s' % titulo_eleitor)
        # print('urna: %s' % urna)
        # print('votos: %s' % votos)
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
                }
            )
        elif (politico == 'Branco' and partido != 'BRANCO') or \
            (politico != 'Branco' and partido == 'BRANCO'):
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
                }
            )
        elif (politico == 'Nulo' and partido != 'NULO') or \
            (politico != 'Nulo' and partido == 'NULO'):
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
                }
            )
        elif politico == 'Branco' and partido == 'BRANCO':
            politico_id 
            branco_bd = Politico.objects.create(
                politico=politico, foto=foto, cargo=cargo,
                partido=partido, num_partido=num_partido, branco=True,
                nulo=False, abstencao=False, te_eleitor=titulo_eleitor,
                urna=urna,
            )
            branco_bd.save()
            return render(request, 'votar/registrar-voto.html',
                {
                    'num_partido_1': branco_bd.num_partido[0],
                    'num_partido_2': branco_bd.num_partido[1],
                    'politico': branco_bd.politico,
                    'partido': branco_bd.partido,
                    'cargo': branco_bd.cargo,
                    'foto': branco_bd.foto,
                }
            )
        elif politico == 'Nulo' and partido == 'NULO':
            nulo_bd = Voto.objects.create(
                politico=politico, foto=foto, cargo=cargo,
                partido=partido, num_partido=num_partido, branco=False,
                nulo=True, abstencao=False, te_eleitor=titulo_eleitor,
                urna=urna,
            )
            nulo_bd.save()
            return render(request, 'votar/registrar-voto.html',
                {
                    'num_partido_1': nulo_bd.num_partido[0],
                    'num_partido_2': nulo_bd.num_partido[1],
                    'politico': nulo_bd.politico,
                    'partido': nulo_bd.partido,
                    'cargo': nulo_bd.cargo,
                    'foto': nulo_bd.foto,
                }
            )
        elif (politico != 'Branco' and partido != 'BRANCO') and \
            (politico != 'Nulo' and partido != 'NULO'):
            print('urna: %s' % urna)
            politico_bd = Voto.objects.create(
                politico=politico, foto=foto, cargo=cargo,
                partido=partido, num_partido=num_partido, branco=False,
                nulo=False, abstencao=False, te_eleitor=titulo_eleitor,
                urna=urna,
            )
            politico_bd.save()
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
                    'urna': urna,
                    'urna_id': urna_id,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )
    else:
        return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'urna_id': urna_id,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )        

#return HttpResponse('<h1>Político: %s</h1><br><h2>Partido: %s</h2>' % (politico_bd, partido))
# return HttpResponse('<h1>Político: %s</h1>' % politico_bd)
# 'titulo_eleitor': titulo_eleitor,
# 'urna': urna,
# 'votos': votos,
# 'cargo': cargo,
# 'erro': True,
# 'politico': politico,
# 'partido': partido,
# 'num_partido': num_partido,
# 'foto': foto,
# def registrar(request):
# pass
# return HttpResponse('<h1>%s</h1>' % politico)
