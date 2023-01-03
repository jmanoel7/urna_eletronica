from django.db import models
from urna.models import Urna, Voto

class Eleitor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    data_nascimento = models.DateField()
    titulo_eleitor = models.CharField(max_length=12, unique=True)
    zona = models.CharField(max_length=4)
    secao = models.CharField(max_length=4)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    data_emissao = models.DateField()
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='eleitores')
    voto = models.ForeignKey(Voto, on_delete=models.PROTECT, related_name='eleitores',
        blank=True, null=True, default=None)

    def __str__(self):
        return self.nome
