from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profiles', on_delete=models.CASCADE)
    description = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.pk})


class PointsUserList(models.Model):
    profile = models.ForeignKey(Profile, related_name='admiradores', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BlockedList(models.Model):
    profile = models.ForeignKey(Profile, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
