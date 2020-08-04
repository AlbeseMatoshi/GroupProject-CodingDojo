from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from app_one.models import *
from app_bookings.models import *

#DEVELOPMENT ONLY
## FILE TO HELP US DEVELOP OTHER PARTS
## USER WILL NOT HAVE ACCESS TO THESE ACTIONS
def show_dashboard(request):
    try:
        a = User.objects.get(id=request.session['uid'])
        if a.role == 0:
            return redirect('/')
    except:
        return redirect('/')
    context = {
        'movies' : Movie.objects.all(),
        'rooms' : CinoRoom.objects.all(),
        'user' : User.objects.filter(role=0),
        'logged_user': User.objects.get(id=request.session['uid'])
    }
    return render(request, 'dashboard.html', context)

def add_movie(request):
    errors = Movie.objects.movie_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/management')
    else:
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

# Events
def add_event(request):
    errors = Event.objects.event_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/management')
    else:
        event = Event.objects.create(title=request.POST['title'], desc=request.POST['description'])
        if 'cover_image' in request.FILES != None:
            pic = request.FILES['cover_image']
            fs = FileSystemStorage()
            fs.save(pic.name, pic)
            event.cover_image = pic
            event.save()
        return redirect('/')

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('/')

def add_cino_room(request):
    errors = CinoRoom.objects.room_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/management')
    else:
        room_id = CinoRoom.objects.create(room=request.POST['room_name'])
        seats = []
        rows = ['A', 'B', 'C', 'D', 'E']

        for row_item in rows:
            for item in range(10):
                name = f"{item}{row_item}" 
                seats.append(Seat(row=row_item, number=item, room=room_id))
                
        Seat.objects.bulk_create(seats)
        return redirect('/management')

def add_show_time(request):
    errors = ShowTime.objects.showtime_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/management')
    else:
        movie = Movie.objects.get(id=request.POST['movie'])
        room = CinoRoom.objects.get(id=request.POST['cino_room'])
        ShowTime.objects.create(date=request.POST['movie_show_date'], time=request.POST['movie_show_time'], tickets = request.POST['movie_tickets'], price = request.POST['price'], movie=movie, room=room)
        return redirect('/management')

