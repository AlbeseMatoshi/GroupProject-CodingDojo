from django.shortcuts import render
from app_one.models import *

def show_all_bookings(request, user_id):
      context = {}
      if 'uid' in request.session:
            context ={
                  'logged_user': User.objects.get(id=request.session['uid']),
                  'all_bookings': Booking.objects.filter(buyer=user_id),
            }
      return render(request, 'all_bookings.html', context)
