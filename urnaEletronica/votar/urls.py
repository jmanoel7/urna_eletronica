from django.urls import path
from . import views

urlpatterns = [
    # path('votar/', views.votar, name='votar-urna'),
    # path('abstencao/', views.abstencao, name='abstencao'),
    path('eleitor/', views.eleitor, name='selecionar-eleitor'),
]