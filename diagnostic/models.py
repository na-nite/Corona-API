from django.db import models
from app import settings


class Diagnose(models.Model):
    temperature = models.IntegerField()
    pace = models.IntegerField()
    weight = models.IntegerField()
    age = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    answer = models.BooleanField(default=False,blank=True)

    # def diagnose(self):
    #     if self.temperature > 37:
    #         self.answer = True
    #     if self.pace < 55 or self.pace > 85:
    #         self.answer = True
    #     if self.weight > (self.age + 5) or self.weight < (self.age - 5):
    #         self.answer = True

# Create your models here.
