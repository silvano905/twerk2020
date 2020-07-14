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
def reglas_view(request):
    return render(request, 'tip/reglas.html')


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


@login_required
def like_tip(request):
    all_tipsx = MakeTip.objects.filter(author__exact=request.user)
    pksx = MakeTip.objects.filter(author__exact=request.user).values_list('id', flat=True)

    def appendTest(x):
        theList = []
        for i in x:
            theList.append(i)
        return theList

    to_be_deleted = []
    spp = appendTest(pksx)
    while spp:
        s2 = all_tipsx.get(pk=spp[-1])
        s3 = s2.total_down_votes()
        if s3 >= 105:
            to_be_deleted.append(s2.pk)
        spp.pop()
    for x in to_be_deleted:
        MakeTip.objects.filter(author__exact=request.user).get(pk=x).delete()

    is_liked = False
    tip = get_object_or_404(MakeTip, id=request.POST.get('post_id'))
    membership = LikeUserList.objects.filter(user=request.user, post=tip.pk)
    if membership:
        membership.delete()
        is_liked = False

    else:
        LikeUserList.objects.create(user=request.user, post=tip)
        is_liked = True
    return redirect(tip.get_absolute_url())


@login_required
def down_tip(request):
    is_down = False
    tip = get_object_or_404(MakeTip, id=request.POST.get('post_id'))
    membership = DownVoteUserList.objects.filter(user=request.user, post=tip.pk)
    if membership:
        membership.delete()
        is_down = False

    else:
        DownVoteUserList.objects.create(user=request.user, post=tip)
        is_down = True
    return redirect(tip.get_absolute_url())


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





# class tips_list_search(TemplateView, LoginRequiredMixin):
#     login_url = '/login/'
#     template_name = 'tip/tip_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset_list = MakeTip.objects.all()
#
#         query = self.request.GET.get('q')
#         if query is not None:
#             queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(info__icontains=query))
#
#         paginator = Paginator(queryset_list, 36)    # Show 25 contacts per page
#
#         page = self.request.GET.get('page')
#         queryset = paginator.get_page(page)
#
#         ss = self.request.GET
#         print(ss)
#         context = {
#             "post_list": queryset
#         }
#         return context





