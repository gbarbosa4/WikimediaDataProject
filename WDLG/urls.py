from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^populated_cities', views.populated_cities_query, name ='populated_cities'),
    url(r'^start_tour_cities', views.start_tour_cities, name ='start_tour_cities'),
    url(r'^stop_tour_cities', views.stop_tour_cities, name ='stop_tour_cities'),
    url(r'^premierLeague_stadiums', views.premierLeague_stadiums_query, name ='premierLeague_stadiums'),
    url(r'^longest_rivers', views.longest_rivers_query, name ='longest_rivers'),
    url(r'^tour_experience', views.tour_experience, name ='tour_experience'),
    url(r'^line_track_experience', views.line_track_experience, name ='line_track_experience'),
    url(r'^stop_experience', views.stop_experience, name ='stop_experience'),
    url(r'^spanish_airports', views.spanish_airports_query, name ='spanish_airports'),
    url(r'^summer_olympic_games', views.olympic_games_query, name ='summer_olympic_games')
]
