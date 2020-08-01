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
    return show_page(request, 1)


def new_movie(request):
    return render(request, 'new_movie.html')


def log_out(request):
    request.session.clear()
    return redirect('/login_page')

def show_one_movie(request, movie_id):
    context = {
        'movie' : Movie.objects.get(id=movie_id)
    } 
    if 'uid' in request.session: 
        context['logged_user'] = User.objects.get(id=request.session['uid'])
    return render(request, 'show_movie.html', context)



#DEVELOPMENT ONLY
## FILE TO HELP US DEVELOP OTHER PARTS
## USER WILL NOT HAVE ACCESS TO THESE ACTIONS
def show_utils(request):
    return render(request, 'development_utilities.html')

def add_movie(request):
    movie = Movie.objects.create(title=request.POST['title'], desc=request.POST['description'], video_url=request.POST['video_url'])
    if 'cover_image' in request.FILES != None:
        pic = request.FILES['cover_image']
        fs = FileSystemStorage()
        fs.save(pic.name, pic)
        movie.cover_image = pic
        movie.save()
    return redirect('/')

def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect('/')



# Events

def add_event(request):
    event = Events.objects.create(title=request.POST['title'], desc=request.POST['description'])
    if 'cover_image' in request.FILES != None:
        pic = request.FILES['cover_image']
        fs = FileSystemStorage()
        fs.save(pic.name, pic)
        event.cover_image = pic
        event.save()
    return redirect('/')

def delete_event(request, event_id):
    event = Events.objects.get(id=event_id)
    event.delete()
    return redirect('/')

def show_one_event(request, event_id):
    context = {
        'event': Events.objects.get(id=event_id)
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
        'events': Events.objects.all(),
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