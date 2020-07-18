from django.conf.urls import url
from promotions import views
from django.urls import path

app_name = 'promotions'

urlpatterns = [
    url('^updatescores/$', views.update_all_scores_view, name="updatescores"),
    url('^listaganadores/$', views.getAllWinners, name="winners"),
]