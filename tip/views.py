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

User = get_user_model()


@login_required
def crate_tip(request):
    form = MakePostForm()

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

    return render(request, 'tip/maketip_form.html', {'form': form})


class TipUpdateView(UpdateView, LoginRequiredMixin):
    form_class = MakePostForm
    # success_url = reverse_lazy('tips:list')
    model = MakeTip
    template_name = 'tip/maketipupdate.html'

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
        return context


def download_view(request):
    queryset = MakeTip.objects.all()

    context = {
        "post_list": queryset
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
    queryset = MakeTip.objects.all()

    context = {
        "post_list": queryset,

    }
    return render(request, 'tip/tip_list.html', context)


class CreateProfileBeforeSearch(TemplateView, LoginRequiredMixin):
    template_name = 'tip/create_a_profile.html'


def request_services(request):
    return render(request, 'tip/gracias.html')


stripe.api_key = "sk_test_51H4G4xB9GffACqxkKLFJijrVgjhuHV47HEC0OYuLvbwcCfZZbvRcCjIJGddtE9hbhsCzUaOJ5EmwuNNeEWoYC1Xf003Kwq0IBk"


def index(request):
    request_user = Juego.objects.filter(author=request.user)

    return render(request, 'tip/stripe/index.html', {'quinielas': request_user})


def charge(request):
    if request.method == 'POST':
        amount = 5
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
    return render(request, 'tip/stripe/success.html', {'amount': amount})


