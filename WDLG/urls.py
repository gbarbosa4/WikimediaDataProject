from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^populated_cities', views.populated_cities_query, name ='populated_cities'),
    url(r'^start_tour_cities', views.start_tour_cities, name ='start_tour_cities'),
    url(r'^stop_tour_cities', views.stop_tour_cities, name ='stop_tour_cities'),
    url(r'^premierLeague_stadiums', views.premierLeague_stadiums_query, name ='premierLeague_stadiums'),
    url(r'^longest_rivers', views.longest_rivers_query, name ='longest_rivers'),
    url(r'^nile_tour_experience', views.nile_tour_experience, name ='nile_tour_experience'),
    url(r'^nile_line_experience', views.nile_line_experience, name ='nile_line_experience'),
    url(r'^start_nile_experience', views.start_nile_experience, name ='start_nile_experience'),
    url(r'^stop_nile_experience', views.stop_nile_experience, name ='stop_nile_experience'),
    url(r'^spanish_airports', views.spanish_airports_query, name ='spanish_airports'),
    url(r'^summer_olympic_games', views.olympic_games_query, name ='summer_olympic_games')
]
