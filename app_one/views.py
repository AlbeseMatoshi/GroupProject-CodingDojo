from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
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
        'movies' : Movie.objects.all()
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
    movie = Movie.objects.create(title=request.POST['title'], desc=request.POST['description'])
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

  
