from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import MakePostForm
from promotions.models import GamesModel
from .models import MakeTip, LikeUserList, DownVoteUserList
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
from catmessage.models import Juego
import datetime

User = get_user_model()


@login_required
def crate_tip(request):
    form = MakePostForm()

    now = datetime.datetime.now()
    todays_date = now.strftime("%A")
    no_buying = False

    no_buying_days = ["Friday", "Saturday", "Sunday"]
    if todays_date in no_buying_days:
        no_buying = True
    else:
        no_buying = False

    if request.method == "POST":
        form = MakePostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user_tip = form.save(commit=False)
            user_tip.author = request.user

            one = form.cleaned_data['one']
            two = form.cleaned_data['two']
            three = form.cleaned_data['three']
            four = form.cleaned_data['four']
            five = form.cleaned_data['five']
            six = form.cleaned_data['six']
            seven = form.cleaned_data['seven']
            eight = form.cleaned_data['eight']
            nine = form.cleaned_data['nine']

            user_tip.all_choices = one + two + three + four + five + six + seven + eight + nine

            form.save(commit=True)


            # msg_contra = url_pic
            #
            # send_mail('C2020T', 'Bienvenido!', settings.EMAIL_HOST_USER, ['silvanovaldez90@yahoo.com'], html_message=msg_contra,
            #           fail_silently=False)

            return redirect('tips:gracias')
        else:
            form = MakePostForm()

    return render(request, 'tip/maketip_form.html', {'form': form, "no_buying": no_buying})


class TipUpdateView(UpdateView, LoginRequiredMixin):
    form_class = MakePostForm
    # success_url = reverse_lazy('tips:list')
    model = MakeTip
    template_name = 'tip/maketipupdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.datetime.now()
        edit_day = now.strftime("%A")
        no_edit = False

        no_editing_days = ["Friday", "Saturday", "Sunday"]
        if edit_day in no_editing_days:
            no_edit = True
        else:
            no_edit = False

        context['no_editing'] = no_edit
        return context


    def form_valid(self, form):
        post = form.save(commit=False)
        one = form.cleaned_data['one']
        two = form.cleaned_data['two']
        three = form.cleaned_data['three']
        four = form.cleaned_data['four']
        five = form.cleaned_data['five']
        six = form.cleaned_data['six']
        seven = form.cleaned_data['seven']
        eight = form.cleaned_data['eight']
        nine = form.cleaned_data['nine']

        post.all_choices = one + two + three + four + five + six + seven + eight + nine
        post.save()
        return redirect('tips:list')


class TipDeleteView(DeleteView, LoginRequiredMixin):
    model = MakeTip
    success_url = reverse_lazy('tips:list')


class UserTips(ListView, LoginRequiredMixin):



    context_object_name = 'post_list'
    model = MakeTip
    template_name = 'tip/user_tip_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('tips').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.tips.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user.tips.all().count()

        now = datetime.datetime.now()
        edit_day = now.strftime("%A")
        no_more_editing = False

        no_editing_days = ["Friday", "Saturday", "Sunday"]
        if edit_day in no_editing_days:
            no_more_editing = True
        else:
            no_more_editing = False

        context['no_more_editing'] = no_more_editing
        return context


def download_view(request):
    queryset = MakeTip.objects.all()

    now = datetime.datetime.now()
    edit_day = now.strftime("%A")
    no_download = False

    no_download_days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    if edit_day in no_download_days:
        no_download = True
    else:
        no_download = False

    context = {
        "post_list": queryset,
        "no_download": no_download
    }

    return render(request, 'tip/download.html', context)


def filter_list(request, value):
    queryset = MakeTip.objects.all()

    all_games_filter = []

    for games in queryset:
        if games.points == int(value):
            all_games_filter.append(games)

    return render(request, 'tip/top_quinielas/nine.html', {'nine_list': all_games_filter, 'points': value})


def tips_list_search(request):
    user_obj = []
    if request.user.is_authenticated:

        user_obj = MakeTip.objects.filter(author=request.user)
    else:
        user_obj = []

    now = datetime.datetime.now()
    edit_day = now.strftime("%A")
    no_download = False

    no_editing_days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    if edit_day in no_editing_days:
        no_download = True
    else:
        no_download = False


    queryset = MakeTip.objects.all()

    context = {
        "post_list": queryset,
        "no_download": no_download,
        "user_obj": user_obj

    }
    return render(request, 'tip/tip_list.html', context)


class CreateProfileBeforeSearch(TemplateView, LoginRequiredMixin):
    template_name = 'tip/create_a_profile.html'


def request_services(request):
    return render(request, 'tip/gracias.html')


stripe.api_key = "sk_test_51H4G4xB9GffACqxkKLFJijrVgjhuHV47HEC0OYuLvbwcCfZZbvRcCjIJGddtE9hbhsCzUaOJ5EmwuNNeEWoYC1Xf003Kwq0IBk"


def index(request):
    request_user = Juego.objects.filter(author=request.user)
    final_repeated_list = []
    all_my_choices = []
    for my_obj in request_user:
        all_my_choices.append(my_obj.all_choices)

    import collections
    repeated_all_choices = [item for item, count in collections.Counter(all_my_choices).items() if count > 1]
    for i in repeated_all_choices:
        for x in request_user:
            if x.all_choices == i:
                final_repeated_list.append(x.pk)
    print(final_repeated_list)


    total_payment = request_user.count()*2
    total_quinielas = request_user.count()

    x = datetime.datetime.now()
    date_now = x.today()

    now = datetime.datetime.now()
    today_date = now.strftime("%A")
    no_more_buying = False
    # turn to false on monday up

    # uncomment on monday
    # no_more_buying_days = ["Friday", "Saturday", "Sunday"]
    # if today_date in no_more_buying_days:
    #     no_more_buying = True
    # else:
    #     no_more_buying = False

    context = {
        "quinielas": request_user,
        "total": total_payment,
        "total_quinielas": total_quinielas,
        "date": date_now,
        "no_buying": no_more_buying,
        "repeated_list": final_repeated_list
    }

    return render(request, 'tip/stripe/index.html', context)


def charge(request):
    if request.method == 'POST':
        amount = Juego.objects.filter(author=request.user).count()*2
        email = request.user.email
        name = request.user.username
        customer = stripe.Customer.create(
            email=email,
            name=name,
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='usd',
            description="Donation"
        )

    return redirect(reverse('tips:success', args=[amount]))


def successMsg(request, args):
    user_obj = Juego.objects.filter(author=request.user)

    for cart_item in user_obj:
        all_choices = cart_item.one+cart_item.two+cart_item.three+cart_item.four+cart_item.five+cart_item.six+cart_item.seven+cart_item.eight+cart_item.nine
        bought_items = MakeTip.objects.create(one=cart_item.one,
                                              two=cart_item.two,
                                              three=cart_item.three,
                                              four=cart_item.four,
                                              five=cart_item.five,
                                              six=cart_item.six,
                                              seven=cart_item.seven,
                                              eight=cart_item.eight,
                                              nine=cart_item.nine,
                                              author=request.user,
                                              all_choices=all_choices
                               )

        bought_items.save()

        delete_cart_item = Juego.objects.filter(author__exact=request.user, pk=cart_item.pk)
        delete_cart_item.delete()

    amount = args
    total_quinielas = int(amount)//2
    return render(request, 'tip/stripe/success.html', {'amount': amount, "total_quinielas": total_quinielas})


