from django.shortcuts import render, HttpResponse
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
            votos = Voto.objects.filter(cargo = 'Presidente da República')
            return render(request, 'votar/urna.html',
                { 'titulo_eleitor': titulo_eleitor, 'urna': urna, 'votos': votos, 'erro': False }
            )
        abstencao = request.GET.get('abstencao')
        if abstencao:
            return HttpResponse('<h1>%s</h1>' % abstencao)
    elif request.method == 'POST':
        titulo_eleitor = request.POST.get('titulo_eleitor')
        urna = request.POST.get('urna')
        votos = request.POST.get('votos')
        politico = request.POST.get('politico')
        partido = request.POST.get('partido')
        foto = request.POST.get('foto')
        print('politico: %s' % politico)
        print('partido: %s' % partido)
        print('titulo_eleitor: %s' % titulo_eleitor)
        print('urna: %s' % urna)
        print('votos: %s' % votos)
        if not politico or not partido:
            return render(request, 'votar/urna.html',
                {
                    'titulo_eleitor': titulo_eleitor,
                    'urna': urna,
                    'votos': votos,
                    'erro': True,
                    'politico': politico,
                    'partido': partido,
                    'foto': foto,
                }
            )
        return HttpResponse('<h1>Político: %s</h1><br><h2>Partido: %s</h2>' % (politico, partido))
# def registrar(request):
#     if request.method == 'POST':
#         politico = request.POST.get('politico')
#         # politico = request.POST.get('titulo_eleitor')
#     return HttpResponse('<h1>%s</h1>' % politico)
