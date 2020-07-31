from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from app_bookings.models import Event
import bcrypt

def login_page(request):
    return render(request, 'login.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/')
    
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/login_page')


def dashboard(request):
    context = {
        'movies' : Movie.objects.all(),
        'events': Event.objects.all(),
    }
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'index.html', context)


def new_movie(request):
    return render(request, 'new_movie.html')


def log_out(request):
    request.session.clear()
    return redirect('/login_page')

def show_one_movie(request, movie_id):
    context = {
        'movie' : Movie.objects.get(id=movie_id),
        'show_times' : ShowTime.objects.filter(movie=movie_id)
    } 
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'show_movie.html', context)

def show_one_event(request, event_id):
    context = {
        'event' : Event.objects.get(id=event_id)
    } 
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'show_event.html', context)
  

