from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.db.models import Q, F
from datetime import datetime, timedelta, time


class Urna(models.Model):
    zona = models.CharField(max_length=4)
    secao = models.CharField(max_length=4)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return 'Zona: %s, Seção: %s, Município: %s, UF: %s' % (
            self.zona, self.secao, self.municipio, self.uf,
        )


class dataVotacao(models.Model):
    data_votacao = models.DateField(unique=True)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='datas')

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(data_votacao__gte=datetime.now().date()),
                name='data-de-hoje',
            ),
            CheckConstraint(
                check=Q(hora_fim__gt=F('hora_inicio')),
                name='hora_fim_maior',
            ),
            CheckConstraint(
                check=Q(hora_fim__lte=time(23, 55, 0)),
                name='hora_fim_limite',
            ),
            CheckConstraint(
                check=Q(hora_inicio__lte=time(23, 50, 0)),
                name='hora_inicio_limite',
            ),
        ]

        def __str__(self):
            return "Data: %s, Início:%s, Fim:%s" % (
                self.data_votacao.__str__(),
                self.hora_inicio.__str__(),
                self.hora_fim.__str__(),
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
    num_partido = models.CharField(max_length=2, blank=True)
    cargo = models.CharField(max_length=50)
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='politicos')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['partido', 'num_partido', 'cargo'],
                name='cargo_unico',
            ),
            UniqueConstraint(
                fields=['politico', 'partido', 'num_partido', 'cargo'],
                name='politico_unico',
            ),
        ]

    def __str__(self):
        return 'Político: %s, Partido: %s, Número: %s, Cargo: %s' % \
            (self.politico, self.partido, self.num_partido, self.cargo)


class Voto(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='votos')
    politico = models.ForeignKey(Politico, on_delete=models.PROTECT, related_name='votos')
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='votos')
    cargo = models.CharField(max_length=50)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['eleitor', 'cargo'],
                name='voto_unico',
            ),
        ]


class Resultado(models.Model):
    ausentes = models.IntegerField()
    votos_nulo = models.IntegerField()
    votos_branco = models.IntegerField()
    votos_invalidos = models.IntegerField()
    votos_candidato_A = models.IntegerField()
    votos_candidato_B = models.IntegerField()
    votos_validos = models.IntegerField()
    total_votos = models.IntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(votos_invalidos=F('votos_branco')+F('votos_nulo')),
                name='total_invalidos',
            ),
            CheckConstraint(
                check=Q(votos_validos=F('votos_candidato_A')+F('votos_candidato_B')),
                name='total_validos',
            ),
            CheckConstraint(
                check=Q(total_votos=F('votos_validos')+F('votos_invalidos')),
                name='total_votos',
            ),
        ]

