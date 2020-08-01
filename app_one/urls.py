from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('create_user', views.create_user),
    path('login', views.login),
    path('login_page', views.login_page),
    path('new_movie', views.new_movie),
    path('logout', views.log_out),
    path('movie/<int:movie_id>', views.show_one_movie),
    path('event/<int:event_id>', views.show_one_event),
    path('page/<int:page_id>', views.show_page),
    #DEVELOPMENT ONLY
    # path('utils', views.show_utils),
    # path('utils/movie/new', views.add_movie),
    # path('utils/events/new', views.add_event),
    ##
]
