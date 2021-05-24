from django.db import models
from app import settings
from article.models import InternautPost


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(InternautPost, on_delete=models.CASCADE,null=True, blank=True)
    content = models.TextField()
    times = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    def is_parent(self):
        if self.parent is not None:
            return False
        return True
