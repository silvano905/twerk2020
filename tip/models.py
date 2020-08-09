from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class MakeTip(models.Model):
    author = models.ForeignKey(User, related_name='tips', on_delete=models.CASCADE)
    one = models.CharField(max_length=3, default=0)
    two = models.CharField(max_length=63, default=0)
    three = models.CharField(max_length=63, default=0)
    four = models.CharField(max_length=63, default=0)
    five = models.CharField(max_length=63, default=0)
    six = models.CharField(max_length=63, default=0)
    seven = models.CharField(max_length=63, default=0)
    eight = models.CharField(max_length=63, default=0)
    nine = models.CharField(max_length=63, default=0)
    all_choices = models.CharField(max_length=20, blank=True)
    points = models.IntegerField(default=0, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username

    def all_choices_field(self):
        return self.all_choices

    def one_team(self):
        return 'Necaxa vs Mazatlán'

    def two_team(self):
        return 'Pachuca vs León'

    def three_team(self):
        return 'Tigres vs Puebla'

    def four_team(self):
        return 'Querétaro vs Cruz Azul'

    def five_team(self):
        return 'Juárez vs Chivas'

    def six_team(self):
        return 'Pumas vs Monterrey'

    def seven_team(self):
        return 'Tijuana vs San Luis'

    def eight_team(self):
        return 'Atlas vs Toluca'

    def nine_team(self):
        return 'América vs Santos'


    def get_absolute_url(self):
        return reverse('tips:tip_detail', kwargs={'pk': self.pk})


class LikeUserList(models.Model):
    post = models.ForeignKey(MakeTip, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class DownVoteUserList(models.Model):
    post = models.ForeignKey(MakeTip, related_name='members_down', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username