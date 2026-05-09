from django.db import models

class Build(models.Model):
    nome = models.CharField(max_length=100)
    classe = models.CharField(max_length=50)
    nivel = models.IntegerField(default=1)
    transclasse = models.BooleanField(default=False)
    
    # Atributos Base
    forca = models.IntegerField(default=1)
    agilidade = models.IntegerField(default=1)
    vitalidade = models.IntegerField(default=1)
    inteligencia = models.IntegerField(default=1)
    destreza = models.IntegerField(default=1)
    sorte = models.IntegerField(default=1)
    
    # Equipamentos salvos como dicionário JSON (ex: {'topo': {detalhes}, 'mao-direita': {detalhes}})
    equipamentos = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.nome} - {self.classe} (Nv. {self.nivel})"
