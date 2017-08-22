from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^populated_cities', views.populated_cities_query, name ='populated_cities'),
    url(r'^start_tour_cities', views.start_tour_cities, name ='start_tour_cities'),
    url(r'^stop_tour_cities', views.stop_tour_cities, name ='stop_tour_cities'),
    url(r'^premierLeague_stadiums', views.premierLeague_stadiums_query, name ='premierLeague_stadiums'),
    url(r'^start_tour_stadiums', views.start_tour_stadiums, name ='start_tour_stadiums'),
    url(r'^stop_tour_stadiums', views.stop_tour_stadiums, name ='stop_tour_stadiums'),
    url(r'^longest_rivers', views.longest_rivers_query, name ='longest_rivers'),
    url(r'^tour_experience', views.tour_experience, name ='tour_experience'),
    url(r'^line_track_experience', views.line_track_experience, name ='line_track_experience'),
    url(r'^stop_experience', views.stop_experience, name ='stop_experience'),
    url(r'^spanish_airports', views.spanish_airports_query, name ='spanish_airports'),
    url(r'^start_tour_airports', views.start_tour_airports, name ='start_tour_airports'),
    url(r'^stop_tour_airports', views.stop_tour_airports, name ='stop_tour_airports'),
    url(r'^summer_olympic_games_aux', views.olympic_games_query_aux, name ='summer_olympic_games_aux'),
    url(r'^summer_olympic_games', views.olympic_games_query, name ='summer_olympic_games'),
    url(r'^try_demo', views.try_demo, name ='try_demo'),
    url(r'^start_lleida_tour', views.start_lleida_tour, name ='start_lleida_tour'),
    url(r'^start_bayern_tour', views.start_bayern_tour, name ='start_bayern_tour'),
    url(r'^stop_tour_demo', views.stop_tour_demo, name ='stop_tour_demo'),
    url(r'^clear_KML_folder', views.clear_KML_folder, name ='clear_KML_folder'),
    url(r'^stop_current_tour', views.stop_current_tour, name ='stop_current_tour'),
    url(r'^relaunch_LG', views.relaunch_LG, name ='relaunch_LG'),
    url(r'^clear_LG_cache', views.clear_LG_cache, name ='clear_LG_cache')
]
