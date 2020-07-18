from django.conf.urls import url
from tip import views
from django.urls import path

app_name = 'tips'

urlpatterns = [
    url(r'^$', views.tips_list_search, name='list'),
    url(r'^create_tip/$', views.crate_tip, name='create_tip'),
    url(r'^descargar/$', views.download_view, name='download'),
    url(r'^filter/(?P<value>\d+)/$', views.filter_list, name='filter'),
    url(r'^nueve/$', views.nine_view, name='nine'),
    url(r'^ocho/$', views.eight_view, name='eight'),
    url(r'^siete/$', views.seven_view, name='seven'),
    url(r'^seis/$', views.six_view, name='six'),
    url(r'^cinco/$', views.five_view, name='five'),
    url(r'^cuatro/$', views.four_view, name='four'),
    url(r'^tres/$', views.three_view, name='three'),
    url(r'^dos/$', views.two_view, name='two'),
    url(r'^uno/$', views.one_view, name='one'),
    url('thankyou/', views.request_services, name='gracias'),
    url(r'^by/(?P<username>[-\w]+)/$', views.UserTips.as_view(), name='for_user'),
    # url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='single'),

    # url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^tip/(?P<pk>\d+)/edit/$', views.TipUpdateView.as_view(), name='tip_edit'),
    url(r'^tip/(?P<pk>\d+)/remove/$', views.TipDeleteView.as_view(), name='tip_remove'),

    url(r'^tip/(?P<pk>\d+)$', views.tip_details, name='tip_detail'),
    url(r'^warning', views.CreateProfileBeforeSearch.as_view(), name='createprofilebeforeview'),
    url('^stripe/$', views.index, name="stripe"),
    url('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success")
]