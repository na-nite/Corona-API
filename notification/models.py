from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from SuspectedCase.models import SuspectedCase
from app.settings import AUTH_USER_MODEL, EMAIL_HOST
from django.core.mail import send_mail


class Notification(models.Model):
    content = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class CCEmails(models.Model):
    email = models.EmailField()


@receiver(post_save, sender=SuspectedCase)
def notify_moderator(sender, update_fields, instance, **kwargs):
    if kwargs.get('created', False):
        users = get_user_model().objects.all().filter(role=2)
        for user in users:
            Notification.objects.create(user=user
                                        , content='suspected case has been reported')
            send_mail("[Corona-Watch] Nouveau cas signalé",
                      "il y a un cas signalé",
                      EMAIL_HOST,
                      [user.email],
                      fail_silently=False)
