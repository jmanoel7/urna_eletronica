from django.shortcuts import render, redirect
from django.conf import settings

def usuarios(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    usuario = request.user.get_username()
    return redirect('/%s' % usuario)

def gerente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'usuarios/gerente.html')

def assistente(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'usuarios/assistente.html')
