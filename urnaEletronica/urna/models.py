from django.db import models

class Urna(models.Model):
    zona = models.CharField(max_length=4)
    secao = models.CharField(max_length=4)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    ligada = models.BooleanField(default=None, blank=True, null=True)
    hora_inicio = models.DateTimeField(default=None, blank=True, null=True)
    hora_fim = models.DateTimeField(default=None, blank=True, null=True)
    
    def __str__(self):
        return 'Zona: %s, Seção: %s, Município: %s, UF: %s' % (
            self.zona,
            self.secao,
            self.municipio,
            self.uf,
        )

class Voto(models.Model):
    politico = models.CharField(max_length=100, unique=True)
    foto = models.ImageField()
    cargo = models.CharField(max_length=50)
    partido = models.CharField(max_length=10)
    num_partido = models.CharField(max_length=2)
    branco = models.BooleanField(default=None, blank=True, null=True)
    nulo = models.BooleanField(default=None, blank=True, null=True)
    abstencao = models.BooleanField(default=None, blank=True, null=True)
    te_eleitor = models.CharField(max_length=12, blank=True, null=True, default=None)
    urna = models.ForeignKey(Urna, on_delete=models.PROTECT, related_name='votos')

    def __str__(self):
        return 'Político: %s, Cargo: %s' % (self.politico, self.cargo)
