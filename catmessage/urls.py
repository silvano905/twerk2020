from django.conf.urls import url
from catmessage import views

app_name = 'catmessage'

urlpatterns = [
    url(r'^add_message_to/(?P<pk>\d+)/$', views.make_a_message, name='add_message'),
    url(r'^list_messages/(?P<pk>\d+)/$', views.user_detail_messages_view, name='detail_messages'),
    url(r'^profile_block/$', views.block_user, name='block_user'),
    url(r'^juego/(?P<pk>\d+)/editar/$', views.TipUpdateView.as_view(), name='juego_edit'),

]