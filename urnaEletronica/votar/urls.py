from django.urls import path
from . import views

urlpatterns = [
    # path('votar/', views.votar, name='votar-urna'),
    path('eleitor/', views.eleitor, name='selecionar-eleitor'),
]