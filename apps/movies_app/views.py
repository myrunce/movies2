# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from django.contrib import messages
import datetime

# Create your views here.
def login_reg(request):
    return render(request, 'movies_app/index.html')

def process(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        found_users = User.objects.filter(email = request.POST['email'])
        if found_users.count() > 0:
            messages.error(request, 'Email already taken', extra_tags='email')
            return redirect('/')
        else:
            passwordDB = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            created_user = User.objects.create(name = request.POST['name'], username = request.POST['username'] , email = request.POST['email'], password = passwordDB, birthday = request.POST['birth'], zipCode = request.POST['zipCode'])
            request.session['user_id'] = created_user.id
            request.session['user_name'] = created_user.name
            return redirect('/welcome')

def login(request):
    found_users = User.objects.filter(email = request.POST['email'])
    if found_users.count() > 0:
        found_user = found_users.first()
        if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
            request.session['user_id'] = found_user.id
            request.session['user_name'] = found_user.name
            return redirect('/welcome')
        else:
            messages.error(request, 'Login Failed', extra_tags='fail')
            return redirect('/')
    else:
        messages.error(request, 'Login Failed', extra_tags='fail')
        return redirect('/')

def welcome(request):
    return render(request, 'movies_app/welcome.html', {'current': User.objects.get(id = request.session['user_id']).zipCode})

# def watch(request):
#     the_user = movie.objects.get(id = request.session.id)
#     user_watching = Movie.objects.create(movie = name of movie, users = the_user)
#     return redirect('/')

def find_users(request):
    users = User.objects.filter(name__startswith = request.POST['find_name'])
    if users.count() < 2:
        users = User.objects.get(name__startswith = request.POST['find_name'])
    print users
    return HttpResponse(users)

def movie(request, movie_id):
    context = {
    'current': User.objects.get(id = request.session['user_id']).zipCode,
    'movie_id': str(movie_id)
    }
    print context['current']
    return render(request, 'movies_app/movie.html', context)
