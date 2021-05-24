from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

from app import settings


class Post(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'

    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING, )

    class Meta:
        abstract = True


class InternautPost(Post):
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='vedios')

    def __str__(self):
        return self.title

    def soft_del(self):
        self.deleted = True
        self.save()


class WriterPost(Post):
    content = models.TextField()
    file = models.FileField(upload_to='media', default='N/A')

    def __str__(self):
        return self.title

    def soft_del(self):
        self.deleted = True
        self.save()

    def display_content(self):
        return mark_safe(self.content)
