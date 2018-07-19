
from django.conf.urls import url

from . import views

app_name="netflixclone"
urlpatterns = [
    # ex: /movie/detail
    url('favorites/<int:user_id>', views.favorites, name='favorites'),
    # ex: /polls/5/
    url('detail/<int:movie_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    url('search', views.search, name='search'),
    url('', views.index, name='index'),
    url('login', views.login, name="login"),
    url('add_favorite', views.add_favorite, name="add_favorite"),
    url('remove_favorite', views.remove_favorite, name='remove_favorite'),
    url('register', views.register, name="register"),
    url('logout', views.logout, name="logout"),
]