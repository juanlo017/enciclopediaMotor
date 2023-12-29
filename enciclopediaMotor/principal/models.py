from django.db import models

class PokemonType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    generation = models.CharField(max_length=100)
    weight = models.FloatField(max_length=100)
    height = models.FloatField(max_length=100)
    color = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=100)

    types = models.ManyToManyField(PokemonType)

    def __str__(self):
        return self.name
