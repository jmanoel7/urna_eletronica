from django.db import models

class Urna(models.Model):
    zona = models.CharField(max_length=4)
    secao = models.CharField(max_length=4)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    ligada = models.BooleanField()
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    
    def __str__(self):
        return 'Zona: %s, Seção: %s, Município: %s, UF: %s' % (
            self.zona,
            self.secao,
            self.municipio,
            self.uf,
        )
