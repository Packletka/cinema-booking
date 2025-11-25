from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('sessions/', views.session_list, name='session_list'),
    path('booking/<int:session_id>/', views.booking, name='booking'),
]