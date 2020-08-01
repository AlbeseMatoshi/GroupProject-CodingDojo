from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import numpy as np

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
        user=User.objects.create(first_name=request.POST['first_name'],
                                 last_name=request.POST['last_name'], email=request.POST['email'],
                                 password= password, role = request.POST['role'])
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
    return show_page(request, 1)


def new_movie(request):
    return render(request, 'new_movie.html')


def log_out(request):
    request.session.clear()
    return redirect('/login_page')

def show_one_movie(request, movie_id):
    context = {
        'movie' : Movie.objects.get(id=movie_id),
        'showtimes' : ShowTime.objects.filter(movie=movie_id)
    } 
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'show_movie.html', context)


def show_one_event(request, event_id):
    context = {
        'event': Event.objects.get(id=event_id)
    } 
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'show_event.html', context)


def show_page(request, page_id):
    movies_per_page = 12
    total_pages = int(len(Movie.objects.all()) / movies_per_page) + 1
    print(total_pages)
    if page_id > total_pages:
        return HttpResponse("error 404")
    elif page_id == total_pages and len(Movie.objects.all()) % movies_per_page > 0:
      movies_per_page = len(Movie.objects.all()) % movies_per_page

    context = {
        'movies': Movie.objects.all()[(page_id-1)*12:(page_id-1)*12+movies_per_page],
        'events': Event.objects.all(),
        'newest_movies': Movie.objects.all(),
        'total_pages': total_pages,
        'current_page': page_id
    }
    if 'uid' in request.session:
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'index.html', context)

def search(request):
    if "q" in request.GET:
        context = {
            "movies": Movie.objects.filter(title__contains=request.GET["q"])
        }
        return render(request, "index.html", context)
    else:
        return redirect('/')
    

# def tickets(request, movie_id):
#     request.session['quantity'] = int(request.POST['tickets'])
#     movie = Movie.objects.get(id=movie_id)
    
#     price =  * request.session['quantity']
#     booking = Booking.objects.create(tickets = request.POST['tickets'], price = price)
#     return redirect('/booking')