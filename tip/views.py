from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import MakePostForm
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

            print(user_tip.all_choices)
            form.save(commit=True)


            # msg_contra = url_pic
            #
            # send_mail('C2020T', 'Bienvenido!', settings.EMAIL_HOST_USER, ['silvanovaldez90@yahoo.com'], html_message=msg_contra,
            #           fail_silently=False)

            return redirect('tips:gracias')
        else:
            form = MakePostForm()

    return render(request, 'tip/maketip_form.html', {'form': form})


@login_required
def tip_details(request, pk):
    post = get_object_or_404(MakeTip, pk=pk)
    is_liked = False
    is_down = False

    if DownVoteUserList.objects.filter(user=request.user, post=post.pk):
        is_down = True

    if LikeUserList.objects.filter(user=request.user, post=post.pk):
        is_liked = True
    context = {
        'post': post,
        # 'is_down': is_down,
        # 'is_liked': is_liked,
        # 'total_likes': post.total_likes(),
        # 'comment_list': Comment.objects.all().order_by('-created_date')
    }
    return render(request, 'tip/tip_detail.html', context)


class TipUpdateView(UpdateView, LoginRequiredMixin):
    form_class = MakePostForm
    success_url = reverse_lazy('tips:list')
    model = MakeTip
    template_name = 'tip/maketipupdate.html'


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
        context['post_user'] = self.post_user
        return context


def nine_view(request):
    queryset = MakeTip.objects.all()
    nine_points_list = []
    nine_points = 'LEEVEVELE'

    for i in queryset:
        if i.all_choices == nine_points:
            nine_points_list.append(i)

    context = {
        "nine_list": nine_points_list
    }

    return render(request, 'tip/top_quinielas/nine.html', context)


def eight_view(request):
    queryset = MakeTip.objects.all()
    eight_points_list = []
    eight_points = 'LEEVEVEL'

    for i in queryset:
        if i.all_choices[0:8] == eight_points:
            eight_points_list.append(i)

    context = {
        "eight_list": eight_points_list
    }
    print(eight_points_list)

    return render(request, 'tip/top_quinielas/eight.html', context)


def seven_view(request):
    queryset = MakeTip.objects.all()
    seven_points_list = []
    seven_points = 'LEEVEVE'

    for i in queryset:
        if i.all_choices[0:7] == seven_points:
            seven_points_list.append(i)

    context = {
        "seven_list": seven_points_list
    }

    return render(request, 'tip/top_quinielas/seven.html', context)

def six_view(request):
    queryset = MakeTip.objects.all()
    six_points_list = []
    six_points = 'LEEVEV'

    for i in queryset:
        if i.all_choices[0:6] == six_points:
            six_points_list.append(i)

    context = {
        "six_list": six_points_list
    }

    return render(request, 'tip/top_quinielas/six.html', context)


def five_view(request):
    queryset = MakeTip.objects.all()
    five_points_list = []
    five_points = 'LEEVE'

    for i in queryset:
        if i.all_choices[0:5] == five_points:
            five_points_list.append(i)

    context = {
        "five_list": five_points_list
    }

    return render(request, 'tip/top_quinielas/five.html', context)


def four_view(request):
    queryset = MakeTip.objects.all()
    four_points_list = []
    four_points = 'LEEV'

    for i in queryset:
        if i.all_choices[0:4] == four_points:
            four_points_list.append(i)

    context = {
        "four_list": four_points_list
    }

    return render(request, 'tip/top_quinielas/four.html', context)


def three_view(request):
    queryset = MakeTip.objects.all()
    three_points_list = []
    three_points = 'LEE'

    for i in queryset:
        if i.all_choices[0:3] == three_points:
            three_points_list.append(i)

    context = {
        "three_list": three_points_list
    }

    return render(request, 'tip/top_quinielas/three.html', context)


def two_view(request):
    queryset = MakeTip.objects.all()
    two_points_list = []
    two_points = 'LV'

    for i in queryset:
        if i.all_choices[0:2] == two_points:
            two_points_list.append(i)

    context = {
        "two_list": two_points_list
    }

    return render(request, 'tip/top_quinielas/two.html', context)


def one_view(request):
    queryset = MakeTip.objects.all()
    one_point_list = []
    one_point = 'V'

    for i in queryset:
        if i.all_choices[0:1] == one_point:
            one_point_list.append(i)

    context = {
        "one_list": one_point_list
    }

    return render(request, 'tip/top_quinielas/one.html', context)


def tips_list_search(request):
    queryset = MakeTip.objects.all()

    nine_points_list = []
    eight_points_list = []
    seven_points_list = []
    six_points_list = []
    five_points_list = []
    four_points_list = []
    three_points_list = []
    two_points_list = []
    one_point_list = []
    zero_points_list = []

    nine_points = 'LEEVEVELE'
    eight_points = 'LEEVEVEL'
    seven_points = 'LEEVEVE'
    six_points = 'LEEVEV'
    five_points = 'LEEVE'
    four_points = 'LEEV'
    three_points = 'LEE'
    two_points = 'LV'
    one_point = 'V'

    for i in queryset:
        if i.all_choices[0] != one_point:
            zero_points_list.append(i)
        if i.all_choices[0:1] == one_point:
            one_point_list.append(i)
        if i.all_choices[0:2] == two_points:
            two_points_list.append(i)
        if i.all_choices[0:3] == three_points:
            three_points_list.append(i)
        if i.all_choices[0:4] == four_points:
            four_points_list.append(i)
        if i.all_choices[0:5] == five_points:
            five_points_list.append(i)
        if i.all_choices[0:6] == six_points:
            six_points_list.append(i)
        if i.all_choices[0:7] == seven_points:
            seven_points_list.append(i)
        if i.all_choices[0:8] == eight_points:
            eight_points_list.append(i)
        if i.all_choices == nine_points:
            nine_points_list.append(i)

    context = {
        "post_list": queryset,
        "nine_list": nine_points_list,
        "eight_list": eight_points_list,
        "seven_list": seven_points_list,
        "five_list": five_points_list,
        "four_list": four_points_list,
        "three_list": three_points_list,
        "two_list": two_points_list,
        "one_list": one_point_list,
        "zero_list": zero_points_list,
        "six_list": six_points_list
    }
    return render(request, 'tip/tip_list.html', context)


class CreateProfileBeforeSearch(TemplateView, LoginRequiredMixin):
    template_name = 'tip/create_a_profile.html'


def request_services(request):
    return render(request, 'tip/gracias.html')


stripe.api_key = "sk_test_51H4G4xB9GffACqxkKLFJijrVgjhuHV47HEC0OYuLvbwcCfZZbvRcCjIJGddtE9hbhsCzUaOJ5EmwuNNeEWoYC1Xf003Kwq0IBk"


# Create your views here.

def index(request):
    return render(request, 'tip/stripe/index.html')


def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
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
    amount = args
    return render(request, 'tip/stripe/success.html', {'amount': amount})


