"""cino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('create_user', views.create_user),
    path('login', views.login),
    path('login_page', views.login_page),
    path('logout', views.log_out),
    path('movie/<int:movie_id>', views.show_one_movie),
    path('movie/<int:movie_id>/delete', views.delete_movie),

    #DEVELOPMENT ONLY
    path('utils', views.show_utils),
    path('utils/movie/new', views.add_movie)
    ##
]
