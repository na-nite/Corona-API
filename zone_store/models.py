from django.db import models


# Create your models here.

class Wilaya(models.Model):
    code = models.IntegerField()
    nom = models.CharField(max_length=255)


class Commune(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    nom = models.CharField(max_length=255)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
