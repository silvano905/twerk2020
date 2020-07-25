from .forms import MakeMessageForm
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Profile, BlockedList
from django.contrib.auth import get_user_model
from mousegroup.forms import MakeMessageGroupForm
from mousegroup.models import GroupMessage
from django.contrib.auth.decorators import login_required
from .models import MyMessage, Juego
from .forms import BookModelFormset, BookFormset
from itertools import chain
from django.views.generic import TemplateView, DeleteView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
User = get_user_model()


@login_required
def make_a_message(request, pk):
    recipient = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = MakeMessageForm(data=request.POST, files=request.FILES)
        form2 = MakeMessageGroupForm(request.POST)
        form3 = MakeMessageGroupForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():

            # notify.send(sender=request.user, actor=request.user, recipient=recipient.user, verb='te envió un mensaje', nf_type='message')

            my_message = form.save(commit=False)
            my_message.recipient = recipient
            my_message.author = request.user
            my_message.save()

            request_user_message_group_form2 = form2.save(commit=False)
            foreign_user_message_group_form3 = form3.save(commit=False)

            request_user_message_group_form2.member = recipient
            foreign_user_message_group_form3.member = request.user.profiles

            request_user_message_group_form2.user = request.user
            foreign_user_message_group_form3.user = recipient.user

            if_obj_form2_exists = GroupMessage.objects.filter(member=recipient, user__exact=request.user).exists()
            if_obj_form3_exists = GroupMessage.objects.filter(member=request.user.profiles, user=recipient.user).exists()

            if if_obj_form2_exists and if_obj_form3_exists:
                return redirect('catmessage:detail_messages', pk=recipient.pk)

            elif if_obj_form2_exists == True and if_obj_form3_exists == False:
                foreign_user_message_group_form3.save()
                return redirect('catmessage:detail_messages', pk=recipient.pk)

            elif if_obj_form2_exists == False and if_obj_form3_exists == True:
                request_user_message_group_form2.save()
                return redirect('catmessage:detail_messages', pk=recipient.pk)

            else:
                request_user_message_group_form2.save()
                foreign_user_message_group_form3.save()
                return redirect('catmessage:detail_messages', pk=recipient.pk)
    else:
        form = MakeMessageForm()
        form2 = MakeMessageGroupForm
        form3 = MakeMessageGroupForm

    return render(request, 'mymessage/mymessage_form.html', {'form': form, 'form2': form2, 'form3': form3})


def user_detail_messages_view(request, pk):
    if request.user.profiles.pk == 14:
        # if user is admin
        is_this_admin = True
        profile = get_object_or_404(Profile, pk=pk)
        search_user = MyMessage.objects.filter(author=profile.user, recipient=request.user.profiles)
        request_user = MyMessage.objects.filter(author=request.user, recipient=profile)

    else:
        # if user is not admin
        is_this_admin = False
        profile = get_object_or_404(Profile, pk=14)
        search_user = MyMessage.objects.filter(author=request.user, recipient=14)
        request_user = MyMessage.objects.filter(author=profile.user, recipient=request.user.profiles)

    result_list = sorted(
        chain(search_user, request_user),
        key=lambda instance: instance.created_date)

    context = {
        'is_this_admin': is_this_admin,
        'user_list': profile,
        'both_lists': result_list
    }
    return render(request, 'mymessage/user_detail_messages.html', context)


def block_user(request):
    profile = get_object_or_404(Profile, pk=request.POST.get('post_id'))
    member = BlockedList.objects.filter(user=profile.user, profile=request.user.profiles)
    if member:
        member.delete()

    else:
        BlockedList.objects.create(user=profile.user, profile=request.user.profiles)
    return redirect(profile.get_absolute_url())


class TipUpdateView(UpdateView, LoginRequiredMixin):
    form_class = BookFormset
    # success_url = reverse_lazy('tips:list')
    model = Juego
    template_name = 'mymessage/juegoupdate.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     now = datetime.datetime.now()
    #     edit_day = now.strftime("%A")
    #     no_edit = False
    #
    #     no_editing_days = ["Friday", "Saturday", "Sunday"]
    #     if edit_day in no_editing_days:
    #         no_edit = True
    #     else:
    #         no_edit = False
    #
    #     context['no_editing'] = no_edit
    #     return context


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
        return redirect('tips:stripe')