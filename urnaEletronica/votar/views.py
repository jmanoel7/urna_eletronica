from django.shortcuts import render, HttpResponse
from urna.models import Urna, Voto

def eleitor(request):
    if request.method == 'GET':
        urna = Urna.objects.get(zona='0135', secao='0080', municipio='Goiânia', uf='GO')
        eleitores = urna.eleitores.all()
        return render(request, 'votar/selecionar-eleitor.html',
            { 'eleitores': eleitores, 'urna': urna }
        )
    elif request.method == 'POST':
        voto = request.POST.get('voto')
        if voto:
            titulo_eleitor = request.POST.get('titulo_eleitor')
            urna = request.POST.get('urna')
            votos = Voto.objects.filter(cargo = 'Presidente da República')
            return render(request, 'votar/urna.html',
                { 'titulo_eleitor': titulo_eleitor, 'urna': urna, 'votos': votos }
            )
        abstencao = request.POST.get('abstencao')
        if abstencao:
            return HttpResponse('<h1>%s</h1>' % abstencao)

def registrar(request):
    if request.method == 'POST':
        politico = request.POST.get('politico')
        # politico = request.POST.get('titulo_eleitor')
    return HttpResponse('<h1>%s</h1>' % politico)
