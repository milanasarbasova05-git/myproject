from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Аноним')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title