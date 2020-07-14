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
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username

    def all_choices_field(self):
        return self.all_choices




    # def post_info_summary(self):
    #     len_info = len(self.info)
    #     if len_info > 480:
    #         return self.info[:480]+' . . . .continue'
    #     else:
    #         return self.info

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