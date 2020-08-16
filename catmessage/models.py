from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from accounts.models import Profile
from django.utils.translation import ugettext_lazy as _

class MyMessage(models.Model):
    author = models.ForeignKey(User, related_name='mymessages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('message:for_user', kwargs={'username': self.author.username})

    def filter_by_id(self, obj):
        return obj.id

    class Meta:
        ordering = ['created_date']


class Juego(models.Model):

    class Month(models.TextChoices):
        one = '', "seleciona aqui"
        two = 'L', "L"
        three = 'E', "E"
        four = 'V', 'V'

    author = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)
    one = models.CharField(max_length=3, choices=Month.choices, default=Month.one)
    two = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    three = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    four = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    five = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    six = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    seven = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    eight = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    nine = models.CharField(max_length=63, choices=Month.choices, default=Month.one)
    all_choices = models.CharField(max_length=20, blank=True)
    points = models.IntegerField(default=0, blank=True)
    jornada = models.IntegerField(default=4, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username

    def all_choices_field(self):
        return self.all_choices

    def one_team(self):
        return 'Puebla vs Cruz Azul'

    def two_team(self):
        return 'Juárez vs Necaxa'

    def three_team(self):
        return 'América	vs Tijuana'

    def four_team(self):
        return 'Tigres vs Pachuca'

    def five_team(self):
        return 'Atlas vs Pumas'

    def six_team(self):
        return 'Toluca vs San Luis'

    def seven_team(self):
        return 'Querétaro vs Mazatlán'

    def eight_team(self):
        return 'Santos vs Chivas'

    def nine_team(self):
        return 'León vs Monterrey'
