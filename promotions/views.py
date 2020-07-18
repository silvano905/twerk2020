from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import MakeGamesForm
from .models import GamesModel
# from comments.models import Comment
from django.db.models import Q
from accounts.models import PointsUserList, Profile
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
import stripe
from django.shortcuts import render, redirect
from django.urls import reverse
from tip.models import MakeTip

User = get_user_model()


def getAllWinners(request):
    game_results = get_object_or_404(GamesModel, pk=1).games
    queryset = MakeTip.objects.all()

    a = game_results

    for gm in queryset:
        points = 0
        b = gm.all_choices

        one = a[0:1]
        two = a[1:2]
        three = a[2:3]
        four = a[3:4]
        five = a[4:5]
        six = a[5:6]
        seven = a[6:7]
        eight = a[7:8]
        nine = a[8:9]

        one_user = b[0:1]
        two_user = b[1:2]
        three_user = b[2:3]
        four_user = b[3:4]
        five_user = b[4:5]
        six_user = b[5:6]
        seven_user = b[6:7]
        eight_user = b[7:8]
        nine_user = b[8:9]

        if one_user == one:
            points += 1
        if two_user == two:
            points += 1
        if three_user == three:
            points += 1
        if four_user == four:
            points += 1
        if five_user == five:
            points += 1
        if six_user == six:
            points += 1
        if seven_user == seven:
            points += 1
        if eight_user == eight:
            points += 1
        if nine_user == nine:
            points += 1
        gm.points = points

    winners_list = []
    nine_winner = False
    eight_winner = False
    seven_winner = False
    six_winner = False
    five_winner = False
    winners_list_total = 0

    for gamesx in queryset:
        if gamesx.points == 9:
            nine_winner = True
            winners_list_total = 9
            winners_list.append(gamesx)
        elif gamesx.points == 8:
            if not nine_winner:
                eight_winner = True
                winners_list.append(gamesx)
                winners_list_total = 8
        elif gamesx.points == 7:
            if not nine_winner and not eight_winner:
                seven_winner = True
                winners_list.append(gamesx)
                winners_list_total = 7
        elif gamesx.points == 6:
            if not nine_winner and not eight_winner and not seven_winner:
                six_winner = True
                winners_list.append(gamesx)
                winners_list_total = 6
        elif gamesx.points == 5:
            if not nine_winner and not eight_winner and not seven_winner and not six_winner:
                five_winner = True
                winners_list.append(gamesx)
                winners_list_total = 5

    context = {
        "nine_list": winners_list,
        "point": winners_list_total
    }

    return render(request, 'promotions/all_winners.html', context)
