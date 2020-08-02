from django.urls import path
from . import views

urlpatterns = [
      path('', views.show_dashboard),
      path('movie/new', views.add_movie),
      path('events/new', views.add_event),
      path('<int:movie_id>/delete', views.delete_movie),
      path('room/new', views.add_cino_room),
      path('showtime/new', views.add_show_time)
]