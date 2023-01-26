from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.db.models import Q, F


class Urna(models.Model):
    zona = models.CharField(max_length=4)
    secao = models.CharField(max_length=4)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    data_votacao = models.DateField(default=None, blank=True, null=True)
    hora_inicio = models.TimeField(default=None, blank=True, null=True)
    hora_fim = models.TimeField(default=None, blank=True, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['zona', 'secao', 'municipio', 'uf'],
                name='urna_unica',
            ),
            CheckConstraint(
                check=Q(hora_fim__gt=F('hora_inicio')),
                name='hora_fim_maior',
            ),
        ]

    def __str__(self):
        return 'Zona: %s, Seção: %s, Município: %s, UF: %s' % (
            self.zona, self.secao, self.municipio, self.uf,
        )


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

    def __str__(self):
        return "Nome: %s, Título de Eleitor: %s" % (self.nome, self.titulo_eleitor)

    class Meta:
        verbose_name_plural = "Eleitores"


class Politico(models.Model):
    politico = models.CharField(max_length=100, unique=True)
    foto = models.ImageField(unique=True)
    partido = models.CharField(max_length=10)
    num_partido = models.CharField(max_length=2)
    cargo = models.CharField(max_length=50)
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='politicos')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['partido', 'num_partido', 'cargo'],
                name='cargo_unico',
            ),
        ]

    def __str__(self):
        return 'Político: %s, Partido: %s, Número: %s, Cargo: %s' % \
            (self.politico, self.partido, self.num_partido, self.cargo)


class Voto(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='eleitores')
    politico = models.ForeignKey(Politico, on_delete=models.PROTECT, related_name='politicos')
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='urnas')
    cargo = models.CharField(max_length=50)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['eleitor', 'cargo'],
                name='voto_unico',
            ),
        ]
