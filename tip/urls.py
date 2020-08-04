from django.conf.urls import url
from tip import views
from django.urls import path
from django.views.generic import TemplateView

app_name = 'tips'

urlpatterns = [
    url(r'^$', views.tips_list_search, name='list'),
    url(r'^create_tip/$', views.crate_tip, name='create_tip'),
    url(r'^descargar/$', views.download_view, name='download'),
    url(r'^filter/(?P<value>\d+)/$', views.filter_list, name='filter'),
    url('thankyou/', views.request_services, name='gracias'),
    url(r'^by/(?P<username>[-\w]+)/$', views.UserTips.as_view(), name='for_user'),
    url(r'^tip/(?P<pk>\d+)/edit/$', views.TipUpdateView.as_view(), name='tip_edit'),
    url(r'^tip/(?P<pk>\d+)/remove/$', views.TipDeleteView.as_view(), name='tip_remove'),
    url(r'^warning', views.CreateProfileBeforeSearch.as_view(), name='createprofilebeforeview'),
    url('^stripe/$', views.index, name="stripe"),
    url('charge/', views.charge, name="charge"),
    url('success/', views.successMsg, name="success"),
    url('sitemap.xml', views.site_map, name='sitemap'),
    url('robots.txt', TemplateView.as_view(template_name="tip/robots.txt", content_type="text/plain"),
         name="robots_file")
]