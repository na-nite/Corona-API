from django.db import models

# Create your models here.
from app import settings


class SuspectedCase(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='attachment', default=None, max_length=500, blank=True, null=True)
    USER_TYPE_CHOICES = (
        (1, 'pending'),
        (2, 'accepted'),
        (3, 'rejected'),
    )
    status = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
