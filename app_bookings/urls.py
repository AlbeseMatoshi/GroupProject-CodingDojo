from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>', views.show_all_bookings),
    # path('<int:movie_id>/ticket/new', views.new_ticket_booking)
]
