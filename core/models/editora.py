from django.db import models


class Editora(models.Model):
    nome = models.CharField(max_length=120)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome
