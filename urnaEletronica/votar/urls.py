from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('eleitor/', views.eleitor, name='selecionar-eleitor'),
    path('votar/', views.votar, name='votar-na-urna'),
    # path('registrar/', views.registrar, name='registrar-voto')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)