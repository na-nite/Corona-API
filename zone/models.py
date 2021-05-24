from django.db import models


class Zone(models.Model):
    STATUS_TYPE_CHOICES = (
        ('p', 'pending'),
        ('a', 'approved'),
        ('r', 'rejected'),
    )
    x = models.FloatField()
    y = models.FloatField()
    name = models.CharField(max_length=255)
    dead = models.BigIntegerField(default=0)
    sick = models.BigIntegerField(default=0)
    recovered = models.BigIntegerField(default=0)
    infected = models.BigIntegerField(default=0)
    status = models.CharField(choices=STATUS_TYPE_CHOICES, max_length=1, default='p')


class NationalZone(Zone):
    remarque = models.CharField(blank=True, null=True, max_length=500)
    is_risky = models.BooleanField(default=False)


class InternationalZone(Zone):
    CONTINENT_TYPE_CHOICES = (
        ('AF', 'Africa'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('AU', 'South America'),
    )
    continent = models.CharField(choices=CONTINENT_TYPE_CHOICES, max_length=2, blank=True, null=True)
    carrier = models.BigIntegerField(default=0, blank=True, null=True)
