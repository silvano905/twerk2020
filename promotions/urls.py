from django.conf.urls import url
from promotions import views
from django.urls import path

app_name = 'promotions'

urlpatterns = [
    url('^updatescores/$', views.update_all_scores_view, name="updatescores"),
    url('^listaganadores/$', views.getAllWinners, name="winners"),
    url('^createbook/$', views.create_book_model_form, name="book"),
    url('^identificacion/$', views.search_quiniela, name="details"),
    url(r'^remove/(?P<pk>\d+)/$', views.delete_cart_item, name='cart_remove_item'),

]