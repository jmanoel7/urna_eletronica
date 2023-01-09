from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path('votar/', views.votar, name='votar-urna'),
    # path('abstencao/', views.abstencao, name='abstencao'),
    path('eleitor/', views.eleitor, name='selecionar-eleitor'),
    path('registrar/', views.registrar, name='registrar-voto')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)