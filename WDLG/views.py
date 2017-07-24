from django.shortcuts import render
from django.http import HttpResponseRedirect

from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import os
import time
import netifaces as ni
import locale

from .objects.airport import *
from .objects.city import *
from .objects.clubstadium import *
from .objects.olympicgame import *
from .objects.river import *
from .objects.stadium import *
from .utils.wikiapi import *
from .utils.informationList import *
from .utils.kml_generator import *

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
kml_file_name_longest_rivers = "kml_file_longest_rivers"
kml_file_name_river_tour= "kml_file_nile_tour_experience"
kml_file_name_river_line = "kml_file_nile_line_experience"
kml_file_name_spanish_airports = "kml_file_spanish_airports"
kml_file_name_summer_olympic_games = "kml_file_summer_olympic_game"

file_kmls_txt_path = "kml_tmp/kmls.txt"
file_query_txt_path = "kml_tmp/query.txt"
serverPath = "/var/www/html/"
serverPath_query = "/tmp/"

wikiapi = WikiApi({ 'locale' : 'en'})
informationList = InformationList()

def index(request):
    return render(request, 'WDLG/index.html', {})

def generate_kml(use_case, data_set, kml_name):
	print("Generating KML file ...")
	generator_kml = GeneratorKML(data_set, kml_name ,"")

	if use_case == "Tour Cities":
		kml_file = generator_kml.generateKML_Tour_Cities()

	elif use_case == "Premier League Stadiums":
		kml_file = generator_kml.generateKML_premierLeague_Stadiums()
		write_FlyTo_andSend(kml_file.name)

	elif use_case == "Longest Rivers":
		kml_file = generator_kml.generateKML_Longest_Rivers()

	elif use_case == "Nile Tour Experience":
		kml_file = generator_kml.generateKML_Nile_Tour_Experience(get_nile_dynamic_points())

	elif use_case == "Nile Line Experience":
		kml_file = generator_kml.generateKML_Nile_Line_Experience(get_nile_dynamic_points())

	elif use_case == "Spanish Airports":
		kml_file = generator_kml.generateKML_Spanish_Airports()

	elif use_case == "Summer Olympic Games":
		kml_file = generator_kml.generateKML_Olympic_Games()
		write_FlyTo_andSend(kml_file.name)

	sendKML_ToGalaxy(kml_file, kml_name)

	if use_case == "Premier League Stadiums":
	    time.sleep(10.0)
	    start_tour_premier_league()
	#tour_city_file.save('kmls_management/static/')
	#tour_city_file.file.name = 'kmls_management/static/' + "kml_file_tour_city"
	#tour_city_file.save()

def sendKML_ToGalaxy(kml_file, kml_name):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/kmls.txt", 'w+')
	file.write("http://" + str(ip_server) + ":8000/static/" + "empty_file.kml" + "\n")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

	time.sleep(3)

	file = open("kml_tmp/kmls.txt", 'w+')
	file.write("http://" + str(ip_server) + ":8000/static/" + str(kml_name)+".kml" + "\n")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath)

	print ("KML send!!")

def write_galaxy_ip(galaxy_ip):
    f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/galaxy_ip', 'w+')
    f.write(galaxy_ip)
    f.close()

def get_galaxy_ip():
    f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/galaxy_ip', 'r')
    ip_galaxy_master = f.read()
    f.close()
    print(ip_galaxy_master)
    return ip_galaxy_master

def get_server_ip():
	ni.ifaddresses('eth0')
	ip_server = ni.ifaddresses('eth0')[2][0]['addr']
	return ip_server

def start_tour_cities(request):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Tour cities")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": informationList.get_information_list("Populated_Cities")})

def stop_tour_cities(request):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": informationList.get_information_list("Populated_Cities")})


def write_FlyTo_andSend(kml_file_name):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open(kml_file_name, 'r+')
	line = file.read()
	flyto_text = line.split("<LookAt>")[1].split("</LookAt")[0]
	file.close()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("flytoview=<LookAt>"+flyto_text+"</LookAt>" + '\n')
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
	#time.sleep(10)
    #start_tour_premier_league()
	#file = open("kml_tmp/query.txt", 'w+')
	#file.seek(0)
	#file.truncate()
	#file.write("playtour=Stadium Tour")
	#file.close()
	#os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

def start_tour_premier_league():
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Stadium Tour")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

def start_nile_experience(request):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("playtour=Nile Experience")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponseRedirect('/')

def stop_nile_experience(request):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponseRedirect('/')

def getClubShieldImage(response_xml):
	response_xml = wikiapi.replace(response_xml)
	ind_i = getIndex_substring("infobox",response_xml)
	ind_f = getIndex_substring("scope",response_xml)
	response_xml = response_xml[ind_i:ind_f]
	print("1st cut:... ",response_xml)
	ind_i = getIndex_substring("src=\"",response_xml)
	ind_f = getIndex_substring("\" width",response_xml)
	return "https:"+response_xml[ind_i+len("src=\""):ind_f]

def getIndex_substring(string,resp):
        index = 0
        resp = str(resp)
        if string in resp:
           c = string[0]

           for ch in resp:
               if ch == c:
                  if resp[index:index+len(string)] == string:
                     return index

               index += 1

        return -1

def populated_cities_query(request):

	print ("Obtaining data ...\n")
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

	    image = result["image"]["value"]

	    elevation = result["elevation"]["value"]

	    list_cities.append(City(rank, city, image, population, area, 0, country, elevation))
	    list_cities[rank-1].coordinates(longitude,latitude)

	    rank = rank + 1

	print ("----- CITY INFORMATION -----",list_cities[i])
	print ("RANK: ",list_cities[i].rank)
	print ("CITY: ",list_cities[i].city)
	print ("LATITUDE: ",list_cities[i].latitude)
	print ("LONGITUDE: ",list_cities[i].longitude)
	print ("IMAGE: ",list_cities[i].image)
	print ("POPULATION: ",list_cities[i].population)
	print ("AREA: ",list_cities[i].area)
	print ("DENSITY: ",list_cities[i].density)
	print ("COUNTRY: ",list_cities[i].country)
	print ("ELEVATION: ",list_cities[i].elevation)

	informationList.set_information_list("Populated_Cities",list_cities)

	generate_kml("Tour Cities", list_cities, kml_file_name_tour_city)
	#time.sleep(5)
	return render(request, 'WDLG/indexPopulatedCities.html', {"list_cities": list_cities})

def premierLeague_stadiums_query(request):

	print ("Obtaining data ...\n")
	clubstadium_list = []
	hash_stadium_club = {}
	clubs_list = []
	i = 0
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

	       club_name = result["clubName"]["value"]
	       hash_stadium_club[club_name] = stadium_name

	       club_short_name = result["clubsLabel"]["value"]

	       club_founded = result["founded"]["value"]
	       club_founded = club_founded.split("-")[0]

	       club_coach = result["coachLabel"]["value"]

	       club_city = result["cityLabel"]["value"]

	       stadium_image = result["image"]["value"]

	       stadium_capacity = result["capacity"]["value"]

	       coord = result["coord"]["value"]
	       longitude = coord.split("(")[1].split(" ")[0]
	       latitude = coord.split("(")[1].split(" ")[1]
	       latitude = latitude[:len(latitude) - 1]

	       clubstadium_list.append(ClubStadium(stadium_name, club_short_name, club_name, club_founded, club_coach, club_city, stadium_image, stadium_capacity))
	       clubstadium_list[i].coordinates(longitude,latitude)
	       i=i+1

	for club in hash_stadium_club:
	       clubs_list.append(club)
	clubs_list.sort()
	print("hereeeee")
	club_selected = request.POST.get('combo_list')
	print(club_selected)
	stadium_name = getStadiumByClub(club_selected, hash_stadium_club)

	clubstadium_selected = ""
	club_short_name = ""
	club_shield_image = "https://upload.wikimedia.org/wikipedia/commons/d/d2/Solid_white.png"

	if club_selected != None:
	       for clubstadium in clubstadium_list:
	              if stadium_name == clubstadium.stadiumName:
	                     clubstadium_selected = clubstadium
	                     club_short_name = clubstadium.clubShortName
	                     response_xml = wikiapi.find(club_short_name)
	                     club_shield_image = getClubShieldImage(response_xml)
	                     clubstadium.addClubShield(club_shield_image)

	       generate_kml("Premier League Stadiums", clubstadium_selected, kml_file_name_premierLeague_stadium)
	       print(club_shield_image)
	return render(request, 'WDLG/indexPremierLeagueStadiums.html', {"clubs_list": clubs_list , "stadium_name": stadium_name, "club_shield_image": club_shield_image})

def getStadiumByClub(club, hash_stadium_club):
    for key, value in hash_stadium_club.items():
        if key == club:
            return value

def longest_rivers_query(request):

	print ("Obtaining data ...\n")
	list_rivers = []
	rank = 1
	i = 1
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

	print ("----- RIVER INFORMATION -----")
	print ("RANK: ",list_rivers[i].rank)
	print ("RIVER: ",list_rivers[i].river)
	print ("LATITUDE: ",list_rivers[i].latitude)
	print ("LONGITUDE: ",list_rivers[i].longitude)
	print ("IMAGE: ",list_rivers[i].image)
	print ("LENGTH: ",list_rivers[i].length)
	print ("CONTINENT: ",list_rivers[i].continent)
	print ("ORIGIN: ",list_rivers[i].origin)
	print ("MOUTH: ",list_rivers[i].mouth)
	print ("DISCHARGE: ",list_rivers[i].discharge)

	generate_kml("Longest Rivers", list_rivers, kml_file_name_longest_rivers)

	return render(request, 'WDLG/indexLongestRivers.html')

def nile_tour_experience(request):

	generate_kml("Nile Tour Experience", "", kml_file_name_river_tour)

	return HttpResponseRedirect('/')


def nile_line_experience(request):

	generate_kml("Nile Line Experience", "", kml_file_name_river_line)

	return HttpResponseRedirect('/')


def spanish_airports_query(request):

	print ("Obtaining data ...\n")
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

	print ("----- AIRPORT  INFORMATION -----")
	print ("AIRPORT: ",list_airports[i].airport)
	print ("CITY: ",list_airports[i].city)
	print ("LATITUDE: ",list_airports[i].latitude)
	print ("LONGITUDE: ",list_airports[i].longitude)
	print ("IMAGE: ",list_airports[i].image)
	print ("OPENING: ",list_airports[i].opening)

	generate_kml("Spanish Airports", list_airports, kml_file_name_spanish_airports)

	return render(request, 'WDLG/indexSpanishAirports.html')

def olympic_games_query(request):
    print("OLYMPIC GAMES obtaining data...")

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

            data_list = do_data_list(hash_data)

            for key,value in hash_data_medals.items():
                medal_country_code_list.append(key)

            counter = 0

            with open("static/country_3code.txt", 'r+') as file:
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

            with open("static/coord_olympic_games.txt", 'r+') as file:
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

    else:
        olympic_games_list = informationList.get_information_list("Olympic_Games")

        for key,value in request.POST.items():
            if key == "host_city":
                host_city_selected = value

        for olympic_game in olympic_games_list:
            if (olympic_game.hostCity+" "+str(olympic_game.year)) == host_city_selected:
                olympic_game_selected = olympic_game
                break

        wikiapi.get_url_image(str(olympic_game_selected.year)+" Summer Olympics")

        generate_kml("Summer Olympic Games", olympic_game_selected, kml_file_name_summer_olympic_games)

    return render(request, 'WDLG/indexSummerOlympicGames.html', {"host_city_list": host_city_list})


def get_city_coordenates(city):
    city = "\""+city+"\""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setReturnFormat(JSON)

    sparql.setQuery("""SELECT DISTINCT ?coord
                        WHERE
                        {
                          ?city wdt:P31/wdt:P279* wd:Q515 .
                          ?city wdt:P625 ?coord .
                          ?city rdfs:label ?cityname .

                          FILTER (regex(?cityname,"""+city+"""))
                          FILTER (lang(?cityname) = "en")

                          SERVICE wikibase:label {
                            bd:serviceParam wikibase:language "en" .
                          }

                        }
                        LIMIT 1""")

    queryResults = sparql.query().convert()
    for result in queryResults["results"]["bindings"]:
        coord = result["coord"]["value"]

    return coord


def do_data_list(hash_data):
    for key in hash_data:
        if "city" in key:
            host_city = hash_data[key]
        if "Motto" in key:
            lema = hash_data[key]
        if "Nations" in key:
            num_nations = hash_data[key]
            if len(num_nations)>3:
                num_nations = num_nations.split(" ")[0]
        if "Athletes" in key:
            num_athletes = hash_data[key]
            if len(num_athletes)>6:
                num_athletes = num_athletes.split(" (")[0]
        if "Events" in key:
            num_events = hash_data[key].split(" in")[0]
        if "Opening" in key:
            opening_date = hash_data[key]
        if "Closing" in key:
            closing_date = hash_data[key]
        if "Stadium" in key:
            stadium = hash_data[key]

    data_list = [host_city,lema,num_nations,num_athletes,num_events,opening_date,closing_date,stadium]
    return data_list


def get_nile_dynamic_points():

    data_points = []
    data_points.append("31.257556,2.024952"),

    data_points.append("31.483467,2.498290"),

    data_points.append("31.440261,2.663003"),

    data_points.append("31.419964,2.760786"),

    data_points.append("31.372760,2.853673"),

    data_points.append("31.397276,2.943536"),

    data_points.append("31.402288,2.972821"),

    data_points.append("31.465019,3.038070"),

    data_points.append("31.511250,3.130296"),

    data_points.append("31.586892,3.284156"),

    data_points.append("31.701465,3.492810"),

    data_points.append("31.972723,3.673672"),

    data_points.append("31.936471,3.725370"),

    data_points.append("31.917899,3.751966"),

    data_points.append("31.674478,3.991892"),

    data_points.append("31.563886,4.173441"),

    data_points.append("31.504734,4.331658"),

    data_points.append("31.507455,4.538004"),

    data_points.append("31.581395,4.672313"),

    data_points.append("31.602391,4.819671"),

    data_points.append("31.680052,4.992707"),

    data_points.append("31.732725,5.104461"),

    data_points.append("31.758878,5.190653"),

    data_points.append("31.765643,5.326310"),

    data_points.append("31.771263,5.420828"),

    data_points.append("31.800387,5.516077"),

    data_points.append("31.810994,5.585512"),

    data_points.append("31.779651,5.731332"),

    data_points.append("31.763452,5.788279"),

    data_points.append("31.740378,5.822427"),

    data_points.append("31.720779,5.873488"),

    data_points.append("31.711501,5.904493"),

    data_points.append("31.688444,5.928920"),

    data_points.append("31.655913,5.972593"),

    data_points.append("31.581700,6.106156"),

    data_points.append("31.559706,6.155832"),

    data_points.append("31.545968,6.208479"),

    data_points.append("31.523757,6.248550"),

    data_points.append("31.499872,6.285141"),

    data_points.append("31.485732,6.327516"),

    data_points.append("31.464074,6.351082"),

    data_points.append("31.430849,6.392972"),

    data_points.append("31.420845,6.436590"),

    data_points.append("31.426359,6.473093"),

    data_points.append("31.441154,6.486558"),

    data_points.append("31.428889,6.520578"),

    data_points.append("31.434823,6.550597"),

    data_points.append("31.405135,6.566819"),

    data_points.append("31.380190,6.586652"),

    data_points.append("31.357649,6.610644"),

    data_points.append("31.325236,6.643067"),

    data_points.append("31.319471,6.678704"),

    data_points.append("31.324269,6.702068"),

    data_points.append("31.309753,6.738515"),

    data_points.append("31.294645,6.769401"),

    data_points.append("31.290400,6.792764"),

    data_points.append("31.255232,6.828490"),

    data_points.append("31.213370,6.859107"),

    data_points.append("31.174671,6.852739"),

    data_points.append("31.141107,6.898018"),

    data_points.append("31.110008,6.909979"),

    data_points.append("31.109513,6.931539"),

    data_points.append("31.094379,6.952553"),

    data_points.append("31.061373,6.950475"),

    data_points.append("31.024484,6.956966"),

    data_points.append("30.979755,6.986685"),

    data_points.append("30.917424,6.991829"),

    data_points.append("30.883981,7.021120"),

    data_points.append("30.849305,7.036381"),

    data_points.append("30.822032,7.093943"),

    data_points.append("30.807692,7.112785"),

    data_points.append("30.795752,7.136984"),

    data_points.append("30.768522,7.131287"),

    data_points.append("30.726324,7.192466"),

    data_points.append("30.702694,7.271878"),

    data_points.append("30.674948,7.314139"),

    data_points.append("30.691968,7.329620"),

    data_points.append("30.691216,7.350332"),

    data_points.append("30.664509,7.379118"),

    data_points.append("30.618998,7.414732"),

    data_points.append("30.600358,7.441997"),

    data_points.append("30.559203,7.492083"),

    data_points.append("30.578580,7.511324"),

    data_points.append("30.570961,7.564452"),

    data_points.append("30.538941,7.619865"),

    data_points.append("30.520889,7.661834"),

    data_points.append("30.521273,7.701380"),

    data_points.append("30.529725,7.730285"),

    data_points.append("30.540132,7.783571"),

    data_points.append("30.535847,7.810660"),

    data_points.append("30.523748,7.841228"),

    data_points.append("30.511429,7.896183"),

    data_points.append("30.493634,7.939603"),

    data_points.append("30.450822,7.980625"),

    data_points.append("30.453961,7.998188"),

    data_points.append("30.412258,8.048584"),

    data_points.append("30.401870,8.075549"),

    data_points.append("30.376999,8.107863"),

    data_points.append("30.359429,8.123559"),

    data_points.append("30.346480,8.109187"),

    data_points.append("30.325013,8.151894"),

    data_points.append("30.316955,8.169227"),

    data_points.append("30.327345,8.214481"),

    data_points.append("30.323262,8.239015"),

    data_points.append("30.346133,8.280483"),

    data_points.append("30.354676,8.304373"),

    data_points.append("30.340039,8.352073"),

    data_points.append("30.336750,8.376436"),

    data_points.append("30.360046,8.406614"),

    data_points.append("30.379045,8.430117"),

    data_points.append("30.380437,8.452223"),

    data_points.append("30.354568,8.458941"),

    data_points.append("30.342556,8.488690"),

    data_points.append("30.313406,8.520280"),

    data_points.append("30.282272,8.546240"),

    data_points.append("30.317890,8.609297"),

    data_points.append("30.278822,8.654882"),

    data_points.append("30.265403,8.742132"),

    data_points.append("30.239633,8.778362"),

    data_points.append("30.231960,8.843542"),

    data_points.append("30.223935,8.914162"),

    data_points.append("30.227636,8.979830"),

    data_points.append("30.254366,9.008260"),

    data_points.append("30.296626,9.032352"),

    data_points.append("30.326018,9.074658"),

    data_points.append("30.369400,9.142380"),

    data_points.append("30.391114,9.195635"),

    data_points.append("30.374151,9.235719"),

    data_points.append("30.362927,9.289033"),

    data_points.append("30.338087,9.333593"),

    data_points.append("30.379185,9.387429"),

    data_points.append("30.421961,9.447726"),

    data_points.append("30.469221,9.478093"),

    data_points.append("30.500049,9.514852"),

    data_points.append("30.565687,9.502495"),

    data_points.append("30.670871,9.497252"),

    data_points.append("30.749406,9.470299"),

    data_points.append("30.817003,9.460113"),

    data_points.append("30.920361,9.477712"),

    data_points.append("30.994546,9.476772"),

    data_points.append("31.114997,9.434261"),

    data_points.append("31.275232,9.389019"),

    data_points.append("31.437626,9.335360"),

    data_points.append("31.549378,9.375249"),

    data_points.append("31.619809,9.455622"),

    data_points.append("31.651191,9.522428"),

    data_points.append("31.757655,9.661290"),
    data_points.append("31.965882,9.754955"),

    data_points.append("32.083226,9.864472"),

    data_points.append("32.192450,9.994682"),

    data_points.append("32.278287,10.100968"),

    data_points.append("32.256748,10.397041"),

    data_points.append("32.130381,10.544151"),

    data_points.append("32.288681,10.703216"),

    data_points.append("32.489444,10.871386"),

    data_points.append("32.599159,10.976767"),

    data_points.append("32.655924,11.221475"),

    data_points.append("32.695311,11.494085"),

    data_points.append("32.763951,11.813735"),

    data_points.append("32.756312,12.067875"),
    data_points.append("32.747366,12.117575"),
    data_points.append("32.738210,12.143597"),
    data_points.append("32.743959,12.185942"),
    data_points.append("32.743393,12.206835"),
    data_points.append("32.731711,12.236429"),
    data_points.append("32.751657,12.292921"),
    data_points.append("32.767801,12.344770"),
    data_points.append("32.774832,12.350646"),
    data_points.append("32.795754,12.401931"),
    data_points.append("32.798373,12.423815"),
    data_points.append("32.813687,12.470167"),
    data_points.append("32.813693,12.487907"),
    data_points.append("32.820828,12.503030"),
    data_points.append("32.822304,12.529468"),
    data_points.append("32.811644,12.556356"),
    data_points.append("32.803909,12.574560"),
    data_points.append("32.792818,12.593065"),
    data_points.append("32.787896,12.633289"),
    data_points.append("32.756116,12.738700"),
    data_points.append("32.769275,12.821772"),
    data_points.append("32.760308,12.872509"),
    data_points.append("32.807614,12.948985"),
    data_points.append("32.825300,12.993267"),
    data_points.append("32.256992,14.128014"),
    data_points.append("32.233606,14.775490"),
    data_points.append("32.447688,15.462572"),
    data_points.append("32.534137,15.827350"),
    data_points.append("32.555985,15.979540"),
    data_points.append("32.606200,16.252844"),
    data_points.append("32.691420,16.298705"),
    data_points.append("32.735230,16.401065"),
    data_points.append("32.876603,16.507621"),
    data_points.append("33.003062,16.545000"),
    data_points.append("33.261007,16.660322"),
    data_points.append("33.422618,16.697153"),
    data_points.append("33.613871,16.812488"),
    data_points.append("33.682769,17.124852"),
    data_points.append("33.836987,17.385793"),
    data_points.append("33.910032,18.287541"),
    data_points.append("33.608946,18.738363"),
    data_points.append("33.229080,19.528776"),
    data_points.append("32.905717,19.465126"),
    data_points.append("32.074152,18.844713"),
    data_points.append("31.485268,18.061586"),
    data_points.append("30.769189,18.152132"),
    data_points.append("30.662441,18.516789"),
    data_points.append("30.488566,19.199225"),
    data_points.append("30.304901,19.940748"),
    data_points.append("30.535651,19.937983"),
    data_points.append("30.578123,20.296739"),
    data_points.append("30.385922,20.346564"),
    data_points.append("30.335960,20.807481"),
    data_points.append("30.530797,20.830870"),
    data_points.append("30.656743,21.179723"),
    data_points.append("30.956847,21.484617"),
    data_points.append("32.895308,24.115619"),
    data_points.append("32.917034,24.458874"),
    data_points.append("32.868381,24.879522"),
    data_points.append("32.566098,25.274257"),
    data_points.append("32.612513,25.657618"),
    data_points.append("32.757812,26.108294"),
    data_points.append("32.114840,26.206594"),
    data_points.append("31.764916,26.567864"),
    data_points.append("31.083130,27.276175"),
    data_points.append("30.895969,27.682936"),
    data_points.append("30.784139,28.384844"),
    data_points.append("30.932028,28.885757"),
    data_points.append("31.131317,29.080701"),
    data_points.append("31.217286,29.267223"),
    data_points.append("31.250680,29.491004"),
    data_points.append("31.268597,29.625115"),
    data_points.append("31.268255,29.944050"),
    data_points.append("31.239317,30.106250"),
    data_points.append("31.064125,30.219892"),
    data_points.append("30.970832,30.228635"),
    data_points.append("30.914152,30.334980"),
    data_points.append("30.836827,30.407924"),
    data_points.append("30.829825,30.500183"),
    data_points.append("30.810867,30.591736"),
    data_points.append("30.763143,30.715815"),
    data_points.append("30.779892,30.874593"),
    data_points.append("30.700043,31.084952"),
    data_points.append("30.497006,31.237802"),
    data_points.append("30.517079,31.329670"),
    data_points.append("30.391260,31.441391"),
    data_points.append("30.365029,31.468443")

    return data_points
