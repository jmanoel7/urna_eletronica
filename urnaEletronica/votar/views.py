from django.shortcuts import render, redirect, HttpResponse
from urna.models import Urna, Voto

def eleitor(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0135', secao='0080', municipio='Goiânia', uf='GO')
        eleitores = urna.eleitores.all()
        return render(request, 'votar/selecionar-eleitor.html',
            { 'eleitores': eleitores, 'urna': urna }
        )

def votar(request):
    if request.method == 'GET':
        voto = request.GET.get('voto')
        if voto:
            titulo_eleitor = request.GET.get('titulo_eleitor')
            urna = request.GET.get('urna')
            cargo = 'Presidente da República'
            votos = Voto.objects.filter(cargo)
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'cargo': cargo,
                    'votos': votos,
                    'erro': False
                }
            )
        abstencao = request.GET.get('abstencao')
        if abstencao:
            return HttpResponse('<h1>%s</h1>' % abstencao)
    elif request.method == 'POST':
        titulo_eleitor = request.POST.get('titulo_eleitor')
        urna = request.POST.get('urna')
        votos = request.POST.get('votos')
        cargo = request.POST.get('cargo')
        politico = request.POST.get('politico')
        partido = request.POST.get('partido')
        num_partido = request.POST.get('num_partido')
        foto = request.POST.get('foto')
        # print('politico: %s' % politico)
        # print('partido: %s' % partido)
        # print('titulo_eleitor: %s' % titulo_eleitor)
        # print('urna: %s' % urna)
        # print('votos: %s' % votos)
        if politico is None or partido is None:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )
        if len(politico) == 0 or len(partido) == 0:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )
        if (politico == 'Branco' and partido != 'BRANCO') or \
            (politico != 'Branco' and partido == 'BRANCO'):
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )
        if (politico == 'Nulo' and partido != 'NULO') or \
            (politico != 'Nulo' and partido == 'NULO'):
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'votos': votos,
                    'cargo': cargo,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'num_partido': num_partido,
                    'foto': foto,
                }
            )
        if politico == 'Branco' and partido == 'BRANCO':
            branco_bd = Voto.objects.create(
                politico=politico, foto=foto, cargo=cargo,
                partido=partido, num_partido=num_partido, branco=True,
                nulo=False, abstencao=False, te_eleitor=titulo_eleitor,
                urna=urna
            )
            branco_bd.save()
            return render(request, 'votar/registrar-voto.html',
                {
                    'num_partido_1': branco_bd.num_partido[0],
                    'num_partido_2': branco_bd.num_partido[1],
                    'politico': branco_bd.politico,
                    'partido': branco_bd.partido,
                    'cargo': branco_bd.cargo,
                    'foto': branco_bd.foto
                }
            )
        if politico == 'Nulo' and partido == 'NULO':
            nulo_bd = Voto.objects.create(
                politico=politico, foto=foto, cargo=cargo,
                partido=partido, num_partido=num_partido, branco=True,
                nulo=False, abstencao=False, te_eleitor=titulo_eleitor,
                urna=urna
            )
            nulo_bd.save()
            return redirect('registrar-voto',
                {
                    'num_partido_1': nulo_bd.num_partido[0],
                    'num_partido_2': nulo_bd.num_partido[1],
                    'politico': nulo_bd.politico,
                    'partido': nulo_bd.partido,
                    'cargo': nulo_bd.cargo,
                    'foto': nulo_bd.foto
                }
            )
        politico_bd = Voto.objects.get(politico=politico, partido=partido, num_partido=num_partido)
        if politico_bd is None:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
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
        return HttpResponse('<h1>Político: %s</h1>' % politico_bd)


def registrar(request):
    pass
#     return HttpResponse('<h1>%s</h1>' % politico)
