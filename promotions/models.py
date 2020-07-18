from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class GamesModel(models.Model):
    author = models.ForeignKey(User, related_name='allgames', on_delete=models.CASCADE)
    games = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.author.username
