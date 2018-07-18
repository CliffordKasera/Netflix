from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from urllib.parse import parse_qs

import requests
import json

from .models import User, User_Fav

# Create your views here.

base_url = 'https://api.themoviedb.org/3'
api_key = 'a659b217b5589158a7676f19f52ca75b'

def index(request):
    r = requests.get('{}/movie/latest?api_key={}'.format(base_url, api_key))
    movie = r.json()
    context = {
        'latest': movie,
    }
    if 'user_id' in request.session.keys():
        user_id = request.session['user_id']
        favs = User_Fav.objects.values_list('movie').filter(user_id_id = user_id)
        name = User.objects.get(pk=user_id)
        favs_movies = []
        for fav in favs:
            r = requests.get('{}/movie/{}?api_key={}'.format(base_url, fav[0], api_key))
            if r.status_code == 200:
                movie = r.json()
                favs_movies.append(movie)
        context['favs'] = favs_movies
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def detail(request, movie_id):
    r = requests.get('{}/movie/{}?api_key={}'.format(base_url, movie_id, api_key))
    s = requests.get('{}/movie/{}/similar?api_key={}'.format(base_url, movie_id, api_key))
    if r.status_code == 200:
        movie = r.json()
        template = loader.get_template('detail.html')
        context = {
            'movie': movie,
            'favorite': False,
            'similar': s.json(),
            's': s.status_code
        }
        if 'user_id' in request.session.keys():
            try:
                fav = User_Fav.objects.get(user_id_id = request.session['user_id'], movie = movie_id)
                if fav:
                    context['favorite'] = True
            except:
                context['favorite'] = False
        return HttpResponse(template.render(context, request))
    elif r.status_code == 404:
        return HttpResponse('Not Found')
    else:
        return HttpResponse('API Issues')

def search(request):
    if request.method == 'GET':
        query = request.GET.urlencode()
        q = parse_qs(query)
        r = requests.get('{}/search/movie?api_key={}&query={}'.format(base_url, api_key, q['query']))
        template = loader.get_template('search.html')
        context = {
            'results': r.json(),
            'response': r.status_code
        }
        return HttpResponse(template.render(context, request))

def favorites(request, user_id):
    favs = User_Fav.objects.filter(user_id = user_id)
    name = User.objects.get(pk=user_id)
    return HttpResponse("{} You're voting on Movie {}.".format( name.username, len(favs)))

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username, password=password)
        if user:
            request.session['user_id'] = user.id
        return HttpResponseRedirect('/')


def add_favorite(request):
    if request.method == 'POST':
        if 'user_id' in request.session.keys():
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            movie_id=request.POST['movie_id']
            n_fav = User_Fav(user_id=user, movie=movie_id)
            n_fav.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


def remove_favorite(request):
    if request.method == 'POST':
        if 'user_id' in request.session.keys():
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            movie_id=request.POST['movie_id']
            n_fav = User_Fav.objects.get(user_id=user, movie=movie_id)
            n_fav.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


def register(request):
    if request.method == "POST":
        user = User(username = request.POST['username'], password = request.POST['password'])
        user.save()
        request.session['user_id'] = user.id
        return HttpResponseRedirect('/')
    else:
        template = loader.get_template('register.html')
        context = {}
        return HttpResponse(template.render(context, request))


def logout(request):
    if request.method == "POST":
        if 'user_id' in request.session.keys():
            del request.session['user_id']
            return HttpResponseRedirect('/')
# Create your views here.
