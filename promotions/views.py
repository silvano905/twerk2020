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
from catmessage.models import Juego
from catmessage.forms import BookModelFormset
from django.forms import formset_factory
from django.forms import modelformset_factory
User = get_user_model()


def getAllWinners(request):
    queryset = MakeTip.objects.all()

    final_list = []
    winners_list = []
    nine_winner = []
    eight_winner = []
    seven_winner = []
    six_winner = []
    five_winner = []
    winners_list_total = 0

    for liga in queryset:
        if liga.points == 9:
            nine_winner.append(liga)
        if liga.points == 8:
            eight_winner.append(liga)
        if liga.points == 7:
            seven_winner.append(liga)
        if liga.points == 6:
            six_winner.append(liga)
        if liga.points == 5:
            five_winner.append(liga)

    if nine_winner:
        winners_list_total = 9
        final_list = nine_winner
    elif eight_winner:
        winners_list_total = 8
        final_list = eight_winner
    elif seven_winner:
        winners_list_total = 7
        final_list = seven_winner
    elif six_winner:
        winners_list_total = 6
        final_list = six_winner
    elif five_winner:
        winners_list_total = 5
        final_list = five_winner

    context = {
        "nine_list": final_list,
        "point": winners_list_total
    }

    return render(request, 'promotions/all_winners.html', context)


def update_all_scores_view(request):
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
        #save the change to the database
        gm.save()

    return redirect('tips:list')


def create_book_model_form(request):
    template_name = 'promotions/create_normal.html'
    heading_message = 'Model Formset Demo'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        # formset = modelformset_factory(Juego, fields=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'))
        # formset = formset(queryset=Juego.objects.none())

        formset = BookModelFormset(queryset=Juego.objects.none())
    elif request.method == 'POST':
        formset = BookModelFormset(request.POST)
        if formset.is_valid():
            total = request.POST.get('total_money')

            for form in formset:
                # only save if name is present
                if form:
                    juego_model = form.save(commit=False)
                    form.save(commit=False)
                    juego_model.author = request.user

                    one = form.cleaned_data['one']
                    two = form.cleaned_data['two']
                    three = form.cleaned_data['three']
                    four = form.cleaned_data['four']
                    five = form.cleaned_data['five']
                    six = form.cleaned_data['six']
                    seven = form.cleaned_data['seven']
                    eight = form.cleaned_data['eight']
                    nine = form.cleaned_data['nine']

                    juego_model.all_choices = one + two + three + four + five + six + seven + eight + nine

                    form.save()
            return redirect('tips:stripe')
    return render(request, template_name, {
            'formset': formset,
            'heading': heading_message,
        })


@login_required
def delete_cart_item(request, pk):
    query = Juego.objects.filter(author__exact=request.user, pk=pk)
    query.delete()
    return redirect('tips:stripe')
