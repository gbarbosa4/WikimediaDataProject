from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import os
import time
import netifaces as ni
import locale
import shutil
import cairosvg
import urllib.request

from .objects.airport import *
from .objects.city import *
from .objects.clubstadium import *
from .objects.olympicgame import *
from .objects.river import *
from .objects.stadium import *

from .utils.wikiapi import *
from .utils.informationList import *
from .utils.kml_generator import *
from .utils.project_configuration import *
from .utils.auxiliar_functions import *

NUM_CITIES = 10
NUM_RIVERS = 10
NUM_AIRPORTS = 10

wikidata_instance = "http://www.wikidata.org/entity/"

cities_list = []
clubstadium_list = []
rivers_list = []
airports_list = []

kml_file_name_tour_city = "kml_file_tour_city"
kml_file_name_premierLeague_stadium = "kml_file_premierLeague_stadium"
kml_file_name_tour_premierLeague_stadium = "kml_file_name_tour_premierLeague_stadiums"
kml_file_name_longest_rivers = "kml_file_longest_rivers"
kml_file_name_river_tour= "kml_file_tour_experience"
kml_file_name_river_line_track = "kml_file_line_track_experience"
kml_file_name_spanish_airports = "kml_file_spanish_airports"
kml_file_name_summer_olympic_games = "kml_file_summer_olympic_game"
kml_file_name_lleida_tour_demo = "kml_file_lleida_tour_demo"
kml_file_name_bayern_tour_demo = "kml_file_bayern_tour_demo"

file_kmls_txt_path = "kml_tmp/kmls.txt"
file_query_txt_path = "kml_tmp/query.txt"
serverPath = "/var/www/html/"
serverPath_query = "/tmp/"

wikiapi = WikiApi({ 'locale' : 'en'})
project_configuration = Project_configuration()
informationList = InformationList()
aux_function = Auxiliar_Functions()

def index(request):
    ip_galaxy_master = project_configuration.get_galaxy_ip()
    ip_server = project_configuration.get_server_ip()

    project_configuration.flyTo_initialize()

    file = open("kml_tmp/kmls.txt", 'w+')
    file.write("http://" + str(ip_server) + ":8000/static/utils/" + "empty_file.kml" + "\n")
    file.close()

    os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

    return render(request, 'WDLG/index.html', {})

def start_lleida_tour(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Lleida Tour")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponse(status=204)

def start_bayern_tour(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Bayern Tour")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponse(status=204)

def stop_tour_demo(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponse(status=204)

def clear_KML_folder(request):
    folder = os.getcwd()+"/static/kml/"
    ip_galaxy_master = project_configuration.get_galaxy_ip()
    ip_server = project_configuration.get_server_ip()

    file = open("kml_tmp/kmls.txt", 'w+')
    file.write("http://" + str(ip_server) + ":8000/static/utils/" + "empty_file.kml" + "\n")
    file.close()

    os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

    for file in os.listdir(folder):
        file_path = os.path.join(folder,file)
        print(file_path)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    return HttpResponse(status=204)

def stop_current_tour(request):
    ip_galaxy_master = project_configuration.get_galaxy_ip()
    ip_server = project_configuration.get_server_ip()

    file = open("kml_tmp/query.txt", 'w+')
    file.write("exittour=true")
    file.close()

    os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

    return HttpResponse(status=204)

def relaunch_LG(request):
    ip_galaxy_master = project_configuration.get_galaxy_ip()

    os.system("sshpass -p lqgalaxy ssh lg@" + ip_galaxy_master + \
              " './bin/lg-relaunch '")

    return HttpResponse(status=204)

def clear_LG_cache(request):
    ip_galaxy_master = project_configuration.get_galaxy_ip()

    os.system("sshpass -p lqgalaxy ssh lg@" + ip_galaxy_master + \
              " 'rm -r /home/lg/.googleearth/Cache/* '")

    return HttpResponse(status=204)

def start_tour_cities(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Tour cities")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": informationList.get_information_list("Populated_Cities")})

def stop_tour_cities(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": informationList.get_information_list("Populated_Cities")})

def start_tour_stadiums(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()
	path_stadiums_tour_kmlfolder = "static/kml/kml_file_name_tour_premierLeague_stadiums.kml"

	clubs_list = []
	clubstadium_list = informationList.get_information_list("Premier_League_Stadiums")
	for clubstadium in clubstadium_list:
		clubs_list.append(clubstadium.clubName)
	clubs_list.sort()

	file = open("kml_tmp/kmls.txt", 'w+')
	file.write("http://" + str(ip_server) + ":8000/" + path_stadiums_tour_kmlfolder + "?a=" + str(int(round(time.time()))) + "\n")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

	time.sleep(2.0)

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Tour Stadiums")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
	print("Query.txt send!")
	return render(request, 'WDLG/indexPremierLeagueStadiums.html', {"clubs_list": clubs_list, "club_shield_image": "../static/img/white.png"})

def stop_tour_stadiums(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	clubs_list = []
	clubstadium_list = informationList.get_information_list("Premier_League_Stadiums")
	for clubstadium in clubstadium_list:
		clubs_list.append(clubstadium.clubName)
	clubs_list.sort()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexPremierLeagueStadiums.html', {"clubs_list": clubs_list, "club_shield_image": "../static/img/white.png"})

def tour_experience(request):
	river_name = ""

	for key,value in request.POST.items():
		if key == "river_name":
			river_name = value

	data_points = informationList.get_information_list("Data_Points")
	list_rivers = informationList.get_information_list("Longest_Rivers")

	project_configuration.generate_kml("Tour Experience", data_points, "", kml_file_name_river_tour+"_"+river_name)

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers})

def line_track_experience(request):
	river_name = ""

	for key,value in request.POST.items():
		if key == "river_name":
			river_name = value

	data_points = informationList.get_information_list("Data_Points")
	list_rivers = informationList.get_information_list("Longest_Rivers")

	project_configuration.generate_kml("Line Track Experience", data_points, "", kml_file_name_river_line_track+"_"+river_name)

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers})

def stop_experience(request):
	print("stop experience")
	list_rivers = informationList.get_information_list("Longest_Rivers")

	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponse(status=204)

def start_tour_airports(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Spanish Airports Tour")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexSpanishAirports.html', {"list_airports": informationList.get_information_list("Spanish_Airports")})

def stop_tour_airports(request):
	ip_galaxy_master = project_configuration.get_galaxy_ip()
	ip_server = project_configuration.get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexSpanishAirports.html', {"list_airports": informationList.get_information_list("Spanish_Airports")})

#--------------- EVERY USE CASE HAVE THEIR OWN QUERY ----------------------------

def populated_cities_query(request):

	print ("Obtaining data ...\n")
	project_configuration.flyTo_initialize()
	list_cities = []
	rank = 1
	i = 0
	sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

	sparql.setReturnFormat(JSON)

	sparql.setQuery("""SELECT ?city ?cityLabel (SAMPLE(?population) AS ?population) (SAMPLE(?area) AS ?area)
                       (SAMPLE(?coord) AS ?coord) ?countryLabel (SAMPLE(?image)
                       AS ?image) (SAMPLE(?elevation) AS ?elevation)
                       WHERE
                       {
                        ?city wdt:P31/wdt:P279* wd:Q515 .
                        ?city wdt:P1082 ?population .
                        ?city wdt:P2046 ?area .
                        ?city wdt:P625 ?coord .
                        ?city wdt:P17 ?country .
                        ?city wdt:P18 ?image .
                        ?city wdt:P2044 ?elevation .

                    	SERVICE wikibase:label {
                        	bd:serviceParam wikibase:language "en" .
                      	}
                        }
                        GROUP BY ?city ?cityLabel ?countryLabel
                        ORDER BY DESC(?population)
                        LIMIT """+str(NUM_CITIES))

	queryResults = sparql.query().convert()

	for result in queryResults["results"]["bindings"]:

	    city = result["cityLabel"]["value"]

	    population = result["population"]["value"]
	    population = '{0:,}'.format(int(float(population)))

	    area = result["area"]["value"]
	    if (float(area) > 100000):
            	area = int(float(area))/1000000.0

	    coord = result["coord"]["value"]
	    longitude = coord.split("(")[1].split(" ")[0]
	    latitude = coord.split("(")[1].split(" ")[1]
	    latitude = latitude[:len(latitude) - 1]

	    country = result["countryLabel"]["value"]

	    image_link = result["image"]["value"]
	    image = "../img/cities/image_"+city+".png"

	    elevation = result["elevation"]["value"]

	    list_cities.append(City(rank, city, image, population, area, 0, country, elevation))
	    list_cities[rank-1].coordinates(longitude,latitude)

	    rank = rank + 1

	informationList.set_information_list("Populated_Cities",list_cities)

	project_configuration.generate_kml("Tour Cities", list_cities, "", kml_file_name_tour_city)
	#time.sleep(5)
	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": list_cities})

def premierLeague_stadiums_query(request):

	print ("Obtaining data ...\n")
	project_configuration.flyTo_initialize()
	clubstadium_list = []
	hash_club_shield = ""
	hash_stadium_club = {}
	clubs_list = []
	club_shield_image = "https://upload.wikimedia.org/wikipedia/commons/d/d2/Solid_white.png"

	i = 0

	if len(request.POST) == 0:
		club_selected = ""
		sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

		sparql.setReturnFormat(JSON)

		sparql.setQuery("""SELECT DISTINCT ?clubs ?clubsLabel (SAMPLE (?clubName) AS ?clubName) (SAMPLE (?founded) AS ?founded) (SAMPLE (?coach) AS ?coach) ?coachLabel
		(SAMPLE (?city) AS ?city) ?cityLabel (SAMPLE (?stadium) AS ?stadium) (SAMPLE (?cityinstance) AS ?cityinstance) ?stadiumLabel
		(SAMPLE (?image) AS ?image) (SAMPLE (?coord) AS ?coord) (MAX (?capacity) AS ?capacity)
		WHERE
		{
			wd:Q23009701 wdt:P1923 ?clubs .
			?clubs wdt:P1448 ?clubName .
			?clubs wdt:P571 ?founded .
			?clubs wdt:P286 ?coach .
			?clubs wdt:P131 ?city .
			?city wdt:P31 ?cityinstance .
			?clubs wdt:P115 ?stadium .
			?stadium wdt:P18 ?image .
			?stadium wdt:P625 ?coord .
			?stadium wdt:P1083 ?capacity .

			SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
			}
			GROUP BY ?clubs ?clubsLabel ?coachLabel ?cityLabel ?stadiumLabel
			ORDER BY DESC(?capacity) """)

		queryResults = sparql.query().convert()
		i = 0
		for result in queryResults["results"]["bindings"]:
			cityinstance = result["cityinstance"]["value"]

			if(str(cityinstance) == wikidata_instance+"Q515" or str(cityinstance) == wikidata_instance+"Q3957"
			or str(cityinstance) == wikidata_instance+"Q18511725"):

				stadium_name = result["stadiumLabel"]["value"]
				stadium_name = stadium_name.replace("'","")

				club_name = result["clubName"]["value"]

				club_short_name = result["clubsLabel"]["value"]
				hash_stadium_club[club_name] = stadium_name
				#Watford icon shield pronblem
				if "Watford" in club_name:
				   hash_club_shield = hash_club_shield + club_name + "=" + "../img/Watford_icon.png" + "|"
				else:
				   hash_club_shield = hash_club_shield + club_name + "=" + aux_function.getClubShieldImage(wikiapi.find(club_short_name)) + "|"

				club_founded = result["founded"]["value"]
				club_founded = club_founded.split("-")[0]

				club_coach = result["coachLabel"]["value"]

				club_city = result["cityLabel"]["value"]

				stadium_image_link = result["image"]["value"]
				stadium_image = "../img/stadiums/"+stadium_name.replace(" ","")+".jpg"
				#urllib.request.urlretrieve(stadium_image_link, stadium_name+".jpg")
				stadium_capacity = result["capacity"]["value"]

				coord = result["coord"]["value"]
				longitude = coord.split("(")[1].split(" ")[0]
				latitude = coord.split("(")[1].split(" ")[1]
				latitude = latitude[:len(latitude) - 1]

				clubstadium_list.append(ClubStadium(stadium_name, club_short_name, club_name, club_founded, club_coach, club_city, stadium_image, stadium_capacity))
				clubstadium_list[i].coordinates(longitude,latitude)
				clubstadium_list[i].addClubShield(aux_function.getClubShieldImage(wikiapi.find(club_short_name)))

				if "Watford" in club_name:
				   clubstadium_list[i].addClubShield("../img/Watford_icon.png")

				i=i+1

		hull = False
		swa = False
        #Query exception (Hull and Swansea are not in the result list)
		for club in hash_stadium_club:
		   if club == "Hull City Association Football Club":
		   		   hull = True
		   if club == "Swansea City Association Football Club":
		   		   swa = True

		if hull == False:
		   club_stadium = ClubStadium("KCOM Stadium","Hull City A.F.C.","Hull City Association Football Club",1904,"Leonid Slutski","Kingston upon Hull","../img/stadiums/KCOMStadium.jpg",25404)
		   club_stadium.coordinates(-0.367778,53.746111)
		   #club_stadium.addClubShield("../static/img/Hull_icon.png")
		   clubstadium_list.append(club_stadium)
		   hash_stadium_club["Hull City Association Football Club"] = "KCOM Stadium"
		   hash_club_shield = hash_club_shield + "Hull City Association Football Club" + "=" + "../img/Hull_icon.png" + "|"
		   club_stadium.addClubShield("../img/Hull_icon.png")

		if swa == False:
		   club_stadium = ClubStadium("Liberty Stadium","Swansea City A.F.C.","Swansea City Association Football Club",1912,"Paul Clement","Swansea (Wales)","../img/stadiums/LibertyStadium.jpg",21088)
		   club_stadium.coordinates(-3.9351,51.6422)
		   #club_stadium.addClubShield("../static/img/Swansea_icon.png")
		   clubstadium_list.append(club_stadium)
		   hash_stadium_club["Swansea City Association Football Club"] = "Liberty Stadium"
		   hash_club_shield = hash_club_shield + "Swansea City Association Football Club" + "=" + "../img/Swansea_icon.png" + "|"
		   club_stadium.addClubShield("../img/Swansea_icon.png")

		for club in hash_stadium_club:
		   clubs_list.append(club)
		clubs_list.sort()

		informationList.set_information_list("Premier_League_Stadiums",clubstadium_list)
		informationList.set_information_list("Premier_League_Stadiums_aux",hash_club_shield)
		stadium_name = ""

		ip_galaxy_master = project_configuration.get_galaxy_ip()
		ip_server = project_configuration.get_server_ip()

		#file = open("kml_tmp/kmls.txt", 'w+')
		#file.write("http://" + str(ip_server) + ":8000/static/utils/" + "empty_file.kml" + "\n")
		#file.close()

		#os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

		project_configuration.generate_kml("Tour Premier League Stadiums",clubstadium_list,"",kml_file_name_tour_premierLeague_stadium)

	else:
		clubs_list = []
		clubstadium_list = informationList.get_information_list("Premier_League_Stadiums")
		hash_club_shield = informationList.get_information_list("Premier_League_Stadiums_aux")

		club_selected = request.POST.get("combo_list")

		for clubstadium in clubstadium_list:
			clubs_list.append(clubstadium.clubName)
			if clubstadium.clubName == club_selected:
				stadium_name = clubstadium.stadiumName

		clubs_list.sort()

		if(stadium_name == None):
			stadium_name = ""

		clubstadium_selected = ""
		club_short_name = ""
		i=0

		if club_selected != "":
			for clubstadium in clubstadium_list:
				if stadium_name == clubstadium.stadiumName:
					clubstadium_selected = clubstadium
					club_short_name = clubstadium.clubShortName

					while i<20:
					  club_name = hash_club_shield.split("|")[i].split("=")[0];
					  if club_name == club_selected:
					    club_shield_image = hash_club_shield.split("|")[i].split("=")[1]
					    i=20
					  i=i+1

		project_configuration.generate_kml("Premier League Stadiums", clubstadium_selected, club_shield_image, kml_file_name_premierLeague_stadium)

	return render(request, 'WDLG/indexPremierLeagueStadiums.html', {"clubs_list": clubs_list , "stadium_name": stadium_name, "club_shield_image": str(club_shield_image).replace("../","static/"), "club_selected": club_selected, "hash_club_shield": hash_club_shield} )


def longest_rivers_query(request):

	print ("Obtaining data longest rivers ...\n")
	project_configuration.flyTo_initialize()
	list_rivers = []
	rank = 1
	i = 1
	if len(request.POST) == 0:
		sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

		sparql.setReturnFormat(JSON)

		sparql.setQuery("""SELECT DISTINCT ?river ?riverLabel (MAX(?length) AS ?length) (SAMPLE(?image) AS ?image)
		(SAMPLE(?coord) AS ?coord) ?continentLabel (SAMPLE(?origin) AS ?origin) (SAMPLE(?coord_orig) AS ?coord_orig)
		?mouthLabel (SAMPLE(?coord_mouth) AS ?coord_mouth) (MAX(?discharge) AS ?discharge)
		WHERE
		{
		?river wdt:P31/wdt:P279* wd:Q4022 .
		?river wdt:P2043 ?length .
		?river wdt:P18 ?image .
		?river wdt:P625 ?coord .
		?river wdt:P30 ?continent .
		?river wdt:P885 ?origin .
		?origin wdt:P625 ?coord_orig .
		?river wdt:P403 ?mouth .
		?mouth wdt:P625 ?coord_mouth .
		?river wdt:P2225 ?discharge .

		SERVICE wikibase:label {
		bd:serviceParam wikibase:language "en" .
		}
		}
		GROUP BY ?river ?riverLabel ?continentLabel ?mouthLabel
		ORDER BY DESC(?length)
		LIMIT """+str(NUM_RIVERS))

		queryResults = sparql.query().convert()

		for result in queryResults["results"]["bindings"]:

		   river = result["riverLabel"]["value"]
		   if "River" not in river:
		      river = river +" River"

		   length = result["length"]["value"]

		   image = result["image"]["value"]

		   coord = result["coord"]["value"]
		   longitude = coord.split("(")[1].split(" ")[0]
		   latitude = coord.split("(")[1].split(" ")[1]
		   latitude = latitude[:len(latitude) - 1]

		   continent = result["continentLabel"]["value"]

		   origin_id = result["origin"]["value"]

		   sparql_origin = SPARQLWrapper("https://query.wikidata.org/sparql")
		   sparql_origin.setReturnFormat(JSON)
		   sparql_origin.setQuery("""SELECT DISTINCT (SAMPLE(?label) AS ?label)
								WHERE { <"""+origin_id+"""> rdfs:label ?label
								SERVICE wikibase:label {
								bd:serviceParam wikibase:language "en" .
								}
								FILTER (langMatches( lang(?label), "EN" ) )
								}""")

		   queryResults = sparql_origin.query().convert()

		   for result2 in queryResults["results"]["bindings"]:
		             origin = result2["label"]["value"]

		   coord_origin = result["coord_orig"]["value"]
		   longitude_orig = coord_origin.split("(")[1].split(" ")[0]
		   latitude_orig = coord_origin.split("(")[1].split(" ")[1]
		   latitude_orig = latitude_orig[:len(latitude_orig) - 1]

		   mouth = result["mouthLabel"]["value"]

		   coord_mouth = result["coord_mouth"]["value"]
		   longitude_mouth = coord_mouth.split("(")[1].split(" ")[0]
		   latitude_mouth = coord_mouth.split("(")[1].split(" ")[1]
		   latitude_mouth = latitude_mouth[:len(latitude_mouth) - 1]

		   discharge = result["discharge"]["value"]

		   list_rivers.append(River(rank, river, image, length, continent, origin, mouth, discharge))
		   list_rivers[rank-1].coordinates(latitude,longitude)
		   list_rivers[rank-1].coordinates_origin(latitude_orig,longitude_orig)
		   list_rivers[rank-1].coordinates_mouth(latitude_mouth,longitude_mouth)

		   rank = rank + 1

		informationList.set_information_list("Longest_Rivers",list_rivers)

		project_configuration.generate_kml("Longest Rivers", list_rivers, "", kml_file_name_longest_rivers)

	else:
		list_rivers = informationList.get_information_list("Longest_Rivers")
		river_name = ""
		data_points = []

		for key,value in request.POST.items():
				if key == "river_name":
						river_name = value

		data_points = aux_function.get_river_dynamic_points(river_name)

		informationList.set_information_list("Data_Points",data_points)
		print(river_name+" Points saved.")

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers} )

def spanish_airports_query(request):

	print ("Obtaining data ...\n")
	project_configuration.flyTo_initialize()
	list_airports = []
	rank = 1
	i = 1
	sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

	sparql.setReturnFormat(JSON)

	sparql.setQuery("""SELECT ?airport ?airportLabel (SAMPLE(?coord) AS ?coord) (SAMPLE(?image) AS ?image) (SAMPLE(?opening) AS ?opening) ?cityLabel
        WHERE
        {
          ?airport wdt:P31/wdt:P279* wd:Q1248784 .
          ?airport wdt:P625 ?coord .
          ?airport wdt:P17 ?country .
          ?airport wdt:P18 ?image .
          ?airport wdt:P1619 ?opening .
          ?airport wdt:P931 ?city .

          FILTER(?country = wd:Q29)

          SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en" .
          }

        }

		GROUP BY ?airport ?airportLabel ?cityLabel
		LIMIT """+str(NUM_AIRPORTS))

	queryResults = sparql.query().convert()

	for result in queryResults["results"]["bindings"]:

	    airport = result["airportLabel"]["value"]

	    coord = result["coord"]["value"]
	    longitude = coord.split("(")[1].split(" ")[0]
	    latitude = coord.split("(")[1].split(" ")[1]
	    latitude = latitude[:len(latitude) - 1]

	    image = result["image"]["value"]

	    opening = result["opening"]["value"]
	    opening = opening.split("-")[0]
	    print(opening)

	    city = result["cityLabel"]["value"]

	    list_airports.append(Airport(airport, image, opening, city))
	    list_airports[rank-1].coordinates(longitude,latitude)

	    rank = rank + 1

	informationList.set_information_list("Spanish_Airports",list_airports)

	project_configuration.generate_kml("Spanish Airports", list_airports, "", kml_file_name_spanish_airports)

	return render(request, 'WDLG/indexSpanishAirports.html', {"list_airports": list_airports})

def olympic_games_query(request):
    print("OLYMPIC GAMES obtaining data...")
    project_configuration.flyTo_initialize()
    olympic_games_list = []
    host_city_list = []

    if len(request.POST) == 0:
        year = 2016
        i=0
        while year > 1990:
            medal_country_code_list = []
            medal_country_name_list = []
            result_xml = wikiapi.find(str(year)+" Summer Olympics")
            medals_result_xml = wikiapi.find(str(year)+" Summer Olympics medal table")
            hash_data = wikiapi.scraping_infobox(result_xml)
            hash_data_medals = wikiapi.scraping_medal_table(medals_result_xml)
            data_list = aux_function.do_data_list(hash_data)
            for key,value in hash_data_medals.items():
                medal_country_code_list.append(key)

            counter = 0

            with open("static/utils/country_3code.txt", 'r+') as file:
                while counter<3:
                    for line in file:
                        if str(medal_country_code_list[counter]) in line:
                            hash_data_medals[line.split("|")[1].replace("\n","")] = hash_data_medals.pop(str(medal_country_code_list[counter]))
                            counter = counter + 1
                            if counter == 3:
                                break
                            else:
                                file.seek(0)

            olympic_games_list.append(OlympicGame(data_list[0],year,data_list[1],data_list[2],data_list[3],data_list[4],hash_data_medals,data_list[5],data_list[6],data_list[7]))

            with open("static/utils/coord_olympic_games.txt", 'r+') as file:
                for line in file:
                    if line.split(" =")[0] == data_list[0]:
                        longitude = line.split(" =")[1].split(",")[0]
                        latitude = line.split(" =")[1].split(",")[1]

            olympic_games_list[i].coordinates(longitude,latitude)
            host_city_list.append(data_list[0]+" "+str(year))
            print ("Wait a moment please... year-> ",year)
            year = year - 4
            i = i+1

        informationList.set_information_list("Olympic_Games",olympic_games_list)

        ip_galaxy_master = project_configuration.get_galaxy_ip()
        ip_server = project_configuration.get_server_ip()

        file = open("kml_tmp/kmls.txt", 'w+')
        file.write("http://" + str(ip_server) + ":8000/static/utils/" + "empty_file.kml" + "\n")
        file.close()

        os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

    else:
        print("Summer Olympic Games ...")
        olympic_games_list = informationList.get_information_list("Olympic_Games")

        for key,value in request.POST.items():
            if key == "host_city":
                host_city_selected = value

        for olympic_game in olympic_games_list:
            if (olympic_game.hostCity+" "+str(olympic_game.year)) == host_city_selected:
                olympic_game_selected = olympic_game
                break

        wikiapi.get_url_image(str(olympic_game_selected.year)+" Summer Olympics")

        project_configuration.generate_kml("Summer Olympic Games", olympic_game_selected, "", kml_file_name_summer_olympic_games)

    return render(request, 'WDLG/indexSummerOlympicGames.html', {"host_city_list": host_city_list})

def try_demo(request):
    project_configuration.flyTo_initialize()
    lleida_data = ["../img/cities/image_Lleida.png","Catalonia","Lleida","Segrià",212.3,155,138144,"Àngel Ros i Domingo"]
    bayern_data = ["../img/stadiums/AllianzArena.jpg","FC Bayern Munich","../img/bayern_icon.png","May 2005","340 million","105 x 68 m","Munich",75000]
    project_configuration.generate_kml("Demo Lleida", lleida_data, "", kml_file_name_lleida_tour_demo)
    time.sleep(1.0)
    project_configuration.generate_kml("Demo Bayern", bayern_data, "", kml_file_name_bayern_tour_demo)
    return render(request, 'WDLG/indexTryDemo.html')
