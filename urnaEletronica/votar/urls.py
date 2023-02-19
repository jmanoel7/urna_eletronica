from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('eleitor/', views.eleitor, name='selecionar-eleitor'),
    path('votar/', views.votar, name='votar-na-urna'),
    path('inicio-termino/', views.inicio_termino_votacao, name='inicio-termino-votacao'),
    path('resultado/', views.resultado_votacao, name='resultado-votacao'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
