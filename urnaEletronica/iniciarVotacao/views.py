from django.shortcuts import render

def iniciarVotacao(request):
    return render(request, 'iniciarVotacao/iniciarVotacao.html')
