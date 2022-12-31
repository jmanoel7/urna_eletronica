from django.db import models
from urna.models import Urna

class Politico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    foto = models.ImageField()
    cargo = models.CharField(max_length=50)
    partido = models.CharField(max_length=50)
    num_partido = models.CharField(max_length=2)
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='politicos')

    def __str__(self):
        return self.nome
