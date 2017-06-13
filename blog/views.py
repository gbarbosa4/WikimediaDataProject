from django.shortcuts import render
from django.http import HttpResponseRedirect

from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import os
import time
import netifaces as ni

from WDLG_Project.city import City
from WDLG_Project.clubstadium import ClubStadium
from WDLG_Project.river import River
from WDLG_Project.airport import Airport
from WDLG_Project.olympicgame import OlympicGame
from WDLG_Project.informationList import InformationList
from WDLG_Project.kml_generator import GeneratorKML
from WDLG_Project.wikiapi import WikiApi

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

def post_list(request):
    return render(request, 'blog/post_list.html', {})

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
		print("Summer Olympic Games ",data_set.hostCity)
		kml_file = generator_kml.generateKML_Olympic_Games()

	sendKML_ToGalaxy(kml_file, kml_name)

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

	return HttpResponseRedirect('/')

def stop_tour_cities(request):
	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return HttpResponseRedirect('/')


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
	time.sleep(10)
	file = open("kml_tmp/query.txt", 'w+')
	file.seek(0)
	file.truncate()
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

	    area = result["area"]["value"]
	    if (float(area) > 100000):
            	area = float(area)/1000000.0

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

	generate_kml("Tour Cities", list_cities, kml_file_name_tour_city)
	return HttpResponseRedirect('/')

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

	club_selected = request.POST.get('combo_list')
	stadium_name = getStadiumByClub(club_selected, hash_stadium_club)

	clubstadium_selected = ""
	club_short_name = ""
	club_shield_image = ""

	if club_selected != None:
	       for clubstadium in clubstadium_list:
	              if stadium_name == clubstadium.stadiumName:
	                     clubstadium_selected = clubstadium
	                     club_short_name = clubstadium.clubShortName
	                     response_xml = wikiapi.find(club_short_name)
	                     club_shield_image = getClubShieldImage(response_xml)
	                     clubstadium.addClubShield(club_shield_image)

	       generate_kml("Premier League Stadiums", clubstadium_selected, kml_file_name_premierLeague_stadium)

	return render(request, 'blog/post_list.html', {"clubs_list": clubs_list , "stadium_name": stadium_name, "club_shield_image": club_shield_image})

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

	return HttpResponseRedirect('/')

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

	return HttpResponseRedirect('/')

def olympic_games_query(request):
    print("OLYMPIC GAMES obtaining data...")

    olympic_games_list = []
    host_city_list = []

    if len(request.POST) == 0:
        year = 2016
        i=0
        while year > 1990:
            result_xml = wikiapi.find(str(year)+" Summer Olympics")
            hash_data = wikiapi.scraping_infobox(result_xml)
            data_list = do_data_list(hash_data)
            olympic_games_list.append(OlympicGame(data_list[0],year,data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7]))
            #coord = get_city_coordenates(data_list[0])
            file = open("static/coord_olympic_games.txt", 'r+')
            with open("static/coord_olympic_games.txt", 'r+') as file:
                for line in file:
                    if line.split(" =")[0] == data_list[0]:
                        print (line.split(" =")[1])

            longitude = coord.split("(")[1].split(" ")[0]
            latitude = coord.split("(")[1].split(" ")[1]
            latitude = latitude[:len(latitude) - 1]

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

        generate_kml("Summer Olympic Games", olympic_game_selected, kml_file_name_summer_olympic_games)

    return render(request, 'blog/post_list.html', {"host_city_list": host_city_list})


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
        if "Athletes" in key:
            num_athletes = hash_data[key]
        if "Events" in key:
            num_events = hash_data[key]
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
    data_points.append("31.383740,2.310602"),
    data_points.append("31.452052,2.341847"),
    data_points.append("31.474592,2.377663"),
    data_points.append("31.476492,2.432171"),
    data_points.append("31.493731,2.455718"),
    data_points.append("31.507816,2.459600"),
    data_points.append("31.524799,2.471376"),
    data_points.append("31.529848,2.484625"),
    data_points.append("31.512200,2.497162"),
    data_points.append("31.483467,2.498290"),
    data_points.append("31.463781,2.537379"),
    data_points.append("31.462537,2.563593"),
    data_points.append("31.443409,2.582352"),
    data_points.append("31.425883,2.593863"),
    data_points.append("31.422916,2.599024"),
    data_points.append("31.418574,2.603619"),
    data_points.append("31.413246,2.616201"),
    data_points.append("31.411351,2.623102"),
    data_points.append("31.414769,2.633417"),
    data_points.append("31.424024,2.640135"),
    data_points.append("31.440261,2.663003"),
    data_points.append("31.443909,2.683944"),
    data_points.append("31.451312,2.691060"),
    data_points.append("31.453298,2.706667"),
    data_points.append("31.448174,2.718677"),
    data_points.append("31.443824,2.725422"),
    data_points.append("31.441450,2.733577"),
    data_points.append("31.438920,2.745951"),
    data_points.append("31.437756,2.749210"),
    data_points.append("31.433745,2.753455"),
    data_points.append("31.427030,2.756076"),
    data_points.append("31.419964,2.760786"),
    data_points.append("31.406927,2.762565"),
    data_points.append("31.395618,2.767296"),
    data_points.append("31.387541,2.773988"),
    data_points.append("31.383020,2.780892"),
    data_points.append("31.377699,2.803400"),
    data_points.append("31.371938,2.815283"),
    data_points.append("31.361322,2.833814"),
    data_points.append("31.360182,2.838654"),
    data_points.append("31.363927,2.850300"),
    data_points.append("31.368583,2.852819"),
    data_points.append("31.372760,2.853673"),
    data_points.append("31.376966,2.861967"),
    data_points.append("31.373414,2.868048"),
    data_points.append("31.370872,2.875177"),
    data_points.append("31.371327,2.883032"),
    data_points.append("31.376060,2.892111"),
    data_points.append("31.379926,2.903008"),
    data_points.append("31.389693,2.912246"),
    data_points.append("31.397434,2.920401"),
    data_points.append("31.399125,2.925878"),
    data_points.append("31.398430,2.934174"),
    data_points.append("31.397276,2.943536"),
    data_points.append("31.402235,2.951083"),
    data_points.append("31.406401,2.952265"),
    data_points.append("31.414718,2.950699"),
    data_points.append("31.418491,2.952723"),
    data_points.append("31.418869,2.954900"),
    data_points.append("31.416790,2.958159"),
    data_points.append("31.414754,2.965232"),
    data_points.append("31.409732,2.969863"),
    data_points.append("31.406327,2.970745"),
    data_points.append("31.403385,2.971042"),
    data_points.append("31.402288,2.972821"),
    data_points.append("31.401074,2.980590"),
    data_points.append("31.405802,2.987442"),
    data_points.append("31.422389,2.997078"),
    data_points.append("31.433150,3.004903"),
    data_points.append("31.435491,3.010926"),
    data_points.append("31.436051,3.017641"),
    data_points.append("31.443312,3.021932"),
    data_points.append("31.450141,3.030406"),
    data_points.append("31.458442,3.035199"),
    data_points.append("31.463774,3.036013"),
    data_points.append("31.465019,3.038070"),
    data_points.append("31.465243,3.051940"),
    data_points.append("31.467389,3.056579"),
    data_points.append("31.470188,3.059347"),
    data_points.append("31.473947,3.072157"),
    data_points.append("31.477703,3.087209"),
    data_points.append("31.479198,3.093370"),
    data_points.append("31.485199,3.095026"),
    data_points.append("31.495844,3.107061"),
    data_points.append("31.501011,3.118287"),
    data_points.append("31.506866,3.122139"),
    data_points.append("31.511250,3.130296"),
    data_points.append("31.511679,3.134584"),
    data_points.append("31.509406,3.138197"),
    data_points.append("31.513552,3.153461"),
    data_points.append("31.529750,3.174266"),
    data_points.append("31.533291,3.176382"),
    data_points.append("31.539340,3.184438"),
    data_points.append("31.554077,3.200866"),
    data_points.append("31.569186,3.243269"),
    data_points.append("31.573081,3.258235"),
    data_points.append("31.580275,3.263386"),
    data_points.append("31.586892,3.284156"),
    data_points.append("31.586608,3.298426"),
    data_points.append("31.591093,3.304613"),
    data_points.append("31.601911,3.319068"),
    data_points.append("31.605628,3.321787"),
    data_points.append("31.610490,3.329488"),
    data_points.append("31.614467,3.332577"),
    data_points.append("31.622369,3.354655"),
    data_points.append("31.658802,3.399030"),
    data_points.append("31.657283,3.408975"),
    data_points.append("31.649913,3.430391"),
    data_points.append("31.701465,3.492810"),
    data_points.append("31.809103,3.545806"),
    data_points.append("31.948473,3.542116"),
    data_points.append("31.970955,3.570506"),
    data_points.append("31.988034,3.575518"),
    data_points.append("31.999373,3.575739"),
    data_points.append("32.034639,3.584582"),
    data_points.append("32.038722,3.590586"),
    data_points.append("32.014846,3.620075"),
    data_points.append("31.981757,3.656721"),
    data_points.append("31.969434,3.670059"),
    data_points.append("31.972723,3.673672"),
    data_points.append("31.961062,3.684847"),
    data_points.append("31.949475,3.701008"),
    data_points.append("31.942925,3.712670"),
    data_points.append("31.936471,3.725370"),
    data_points.append("31.935619,3.729132"),
    data_points.append("31.932401,3.732072"),
    data_points.append("31.928232,3.737126"),
    data_points.append("31.926351,3.741063"),
    data_points.append("31.925562,3.743670"),
    data_points.append("31.921987,3.748096"),
    data_points.append("31.917899,3.751966"),
    data_points.append("31.914598,3.759989"),
    data_points.append("31.902202,3.776501"),
    data_points.append("31.847300,3.829955"),
    data_points.append("31.811130,3.862209"),
    data_points.append("31.788965,3.885969"),
    data_points.append("31.775822,3.899015"),
    data_points.append("31.761636,3.915301"),
    data_points.append("31.733543,3.935360"),
    data_points.append("31.713362,3.950976"),
    data_points.append("31.684586,3.974677"),
    data_points.append("31.674478,3.991892"),
    data_points.append("31.663752,4.010325"),
    data_points.append("31.653919,4.019014"),
    data_points.append("31.645185,4.022736"),
    data_points.append("31.628215,4.042292"),
    data_points.append("31.605118,4.077767"),
    data_points.append("31.587551,4.109300"),
    data_points.append("31.577416,4.135197"),
    data_points.append("31.573526,4.142628"),
    data_points.append("31.570386,4.156031"),
    data_points.append("31.567705,4.158843"),
    data_points.append("31.563886,4.173441"),
    data_points.append("31.562729,4.180898"),
    data_points.append("31.552381,4.200921"),
    data_points.append("31.538951,4.216749"),
    data_points.append("31.529968,4.233160"),
    data_points.append("31.526442,4.247458"),
    data_points.append("31.524620,4.251048"),
    data_points.append("31.523985,4.292682"),
    data_points.append("31.522602,4.299858"),
    data_points.append("31.515117,4.317335"),
    data_points.append("31.511568,4.323545"),
    data_points.append("31.504734,4.331658"),
    data_points.append("31.500258,4.347422"),
    data_points.append("31.499139,4.367988"),
    data_points.append("31.505000,4.398421"),
    data_points.append("31.501918,4.401448"),
    data_points.append("31.501429,4.437969"),
    data_points.append("31.502030,4.447817"),
    data_points.append("31.500617,4.460808"),
    data_points.append("31.506897,4.491631"),
    data_points.append("31.513611,4.513403"),
    data_points.append("31.511663,4.524698"),
    data_points.append("31.507455,4.538004"),
    data_points.append("31.507293,4.556186"),
    data_points.append("31.495726,4.581872"),
    data_points.append("31.504398,4.593668"),
    data_points.append("31.518712,4.595685"),
    data_points.append("31.526727,4.611390"),
    data_points.append("31.529444,4.623278"),
    data_points.append("31.536232,4.634352"),
    data_points.append("31.538504,4.642025"),
    data_points.append("31.565726,4.657833"),
    data_points.append("31.574753,4.660368"),
    data_points.append("31.581395,4.672313"),
    data_points.append("31.588165,4.680275"),
    data_points.append("31.592968,4.703004"),
    data_points.append("31.596663,4.709027"),
    data_points.append("31.599968,4.740032"),
    data_points.append("31.598622,4.753847"),
    data_points.append("31.599770,4.766316"),
    data_points.append("31.599208,4.773151"),
    data_points.append("31.602335,4.782275"),
    data_points.append("31.600930,4.791358"),
    data_points.append("31.603969,4.806114"),
    data_points.append("31.602391,4.819671"),
    data_points.append("31.612887,4.824845"),
    data_points.append("31.623170,4.842905"),
    data_points.append("31.631541,4.850707"),
    data_points.append("31.653044,4.900018"),
    data_points.append("31.654985,4.909937"),
    data_points.append("31.659588,4.920111"),
    data_points.append("31.649286,4.925496"),
    data_points.append("31.664919,4.959853"),
    data_points.append("31.675507,4.976498"),
    data_points.append("31.674858,4.984275"),
    data_points.append("31.680052,4.992707"),
    data_points.append("31.687594,5.024522"),
    data_points.append("31.694221,5.036683"),
    data_points.append("31.696483,5.038410"),
    data_points.append("31.698611,5.043016"),
    data_points.append("31.701493,5.044473"),
    data_points.append("31.702759,5.048149"),
    data_points.append("31.706447,5.050157"),
    data_points.append("31.712120,5.059220"),
    data_points.append("31.717206,5.076897"),
    data_points.append("31.729810,5.098955"),
    data_points.append("31.732725,5.104461"),
    data_points.append("31.729409,5.131387"),
    data_points.append("31.736743,5.138496"),
    data_points.append("31.737020,5.144642"),
    data_points.append("31.732896,5.148884"),
    data_points.append("31.734193,5.153333"),
    data_points.append("31.740597,5.156042"),
    data_points.append("31.740351,5.159956"),
    data_points.append("31.738313,5.164062"),
    data_points.append("31.746997,5.183434"),
    data_points.append("31.752896,5.189444"),
    data_points.append("31.758878,5.190653"),
    data_points.append("31.766985,5.200942"),
    data_points.append("31.774909,5.223132"),
    data_points.append("31.783011,5.244344"),
    data_points.append("31.781147,5.260282"),
    data_points.append("31.774097,5.268290"),
    data_points.append("31.770412,5.278437"),
    data_points.append("31.773912,5.286665"),
    data_points.append("31.771731,5.296204"),
    data_points.append("31.766602,5.305360"),
    data_points.append("31.763230,5.318200"),
    data_points.append("31.765643,5.326310"),
    data_points.append("31.770348,5.333228"),
    data_points.append("31.771487,5.339688"),
    data_points.append("31.777709,5.347643"),
    data_points.append("31.779080,5.365800"),
    data_points.append("31.776952,5.368406"),
    data_points.append("31.769078,5.375922"),
    data_points.append("31.767767,5.385727"),
    data_points.append("31.766251,5.394726"),
    data_points.append("31.762147,5.404442"),
    data_points.append("31.772898,5.414058"),
    data_points.append("31.771263,5.420828"),
    data_points.append("31.777319,5.434765"),
    data_points.append("31.777208,5.444642"),
    data_points.append("31.775327,5.452445"),
    data_points.append("31.776029,5.454747"),
    data_points.append("31.776046,5.464496"),
    data_points.append("31.785684,5.466322"),
    data_points.append("31.788570,5.472985"),
    data_points.append("31.785517,5.485130"),
    data_points.append("31.791127,5.498641"),
    data_points.append("31.796990,5.502854"),
    data_points.append("31.800387,5.516077"),
    data_points.append("31.800483,5.534362"),
    data_points.append("31.796892,5.542511"),
    data_points.append("31.799961,5.548600"),
    data_points.append("31.803513,5.549534"),
    data_points.append("31.803262,5.553067"),
    data_points.append("31.801566,5.557666"),
    data_points.append("31.803742,5.574205"),
    data_points.append("31.804311,5.579643"),
    data_points.append("31.807344,5.581814"),
    data_points.append("31.810204,5.582582"),
    data_points.append("31.810994,5.585512"),
    data_points.append("31.809662,5.588321"),
    data_points.append("31.810804,5.592728"),
    data_points.append("31.810982,5.612893"),
    data_points.append("31.807556,5.618358"),
    data_points.append("31.806736,5.627474"),
    data_points.append("31.799515,5.643438"),
    data_points.append("31.799524,5.660708"),
    data_points.append("31.796099,5.678667"),
    data_points.append("31.786339,5.701021"),
    data_points.append("31.783881,5.717914"),
    data_points.append("31.779651,5.731332"),
    data_points.append("31.785406,5.740796"),
    data_points.append("31.783054,5.745009"),
    data_points.append("31.778998,5.748795"),
    data_points.append("31.775704,5.754367"),
    data_points.append("31.777555,5.762730"),
    data_points.append("31.772954,5.777834"),
    data_points.append("31.764844,5.781045"),
    data_points.append("31.759667,5.786778"),
    data_points.append("31.760727,5.788141"),
    data_points.append("31.763012,5.787244"),
    data_points.append("31.763452,5.788279"),
    data_points.append("31.762510,5.789428"),
    data_points.append("31.761514,5.792479"),
    data_points.append("31.759659,5.794663"),
    data_points.append("31.761379,5.798212"),
    data_points.append("31.760406,5.799347"),
    data_points.append("31.754488,5.801978"),
    data_points.append("31.750210,5.806248"),
    data_points.append("31.747505,5.810793"),
    data_points.append("31.742728,5.814944"),
    data_points.append("31.742771,5.819993"),
    data_points.append("31.740378,5.822427"),
    data_points.append("31.742419,5.833041"),
    data_points.append("31.740401,5.834623"),
    data_points.append("31.737386,5.835968"),
    data_points.append("31.737773,5.837893"),
    data_points.append("31.740084,5.839813"),
    data_points.append("31.740771,5.843581"),
    data_points.append("31.734633,5.854122"),
    data_points.append("31.727895,5.859749"),
    data_points.append("31.723804,5.858548"),
    data_points.append("31.722248,5.859978"),
    data_points.append("31.720779,5.873488"),
    data_points.append("31.717120,5.876519"),
    data_points.append("31.717514,5.878593"),
    data_points.append("31.719177,5.881613"),
    data_points.append("31.717471,5.884004"),
    data_points.append("31.713356,5.885658"),
    data_points.append("31.711114,5.888486"),
    data_points.append("31.711629,5.895103"),
    data_points.append("31.710106,5.897568"),
    data_points.append("31.708089,5.900513"),
    data_points.append("31.708776,5.902519"),
    data_points.append("31.711501,5.904493"),
    data_points.append("31.711426,5.907268"),
    data_points.append("31.705343,5.910245"),
    data_points.append("31.702210,5.917427"),
    data_points.append("31.699388,5.919092"),
    data_points.append("31.694485,5.915901"),
    data_points.append("31.692028,5.917075"),
    data_points.append("31.692210,5.918975"),
    data_points.append("31.694452,5.919327"),
    data_points.append("31.695278,5.921781"),
    data_points.append("31.692864,5.925569"),
    data_points.append("31.688444,5.928920"),
    data_points.append("31.680616,5.940334"),
    data_points.append("31.676217,5.940611"),
    data_points.append("31.673653,5.943418"),
    data_points.append("31.667602,5.938787"),
    data_points.append("31.661326,5.944304"),
    data_points.append("31.660758,5.955386"),
    data_points.append("31.661606,5.961692"),
    data_points.append("31.657833,5.965369"),
    data_points.append("31.657533,5.968186"),
    data_points.append("31.658263,5.971803"),
    data_points.append("31.655913,5.972593"),
    data_points.append("31.649765,5.969317"),
    data_points.append("31.647656,5.969959"),
    data_points.append("31.640622,5.983728"),
    data_points.append("31.636848,5.994201"),
    data_points.append("31.619288,6.016220"),
    data_points.append("31.617760,6.034139"),
    data_points.append("31.602216,6.063607"),
    data_points.append("31.591077,6.078641"),
    data_points.append("31.593427,6.086488"),
    data_points.append("31.587031,6.099832"),
    data_points.append("31.581700,6.106156"),
    data_points.append("31.584184,6.115446"),
    data_points.append("31.582172,6.115848"),
    data_points.append("31.574842,6.113697"),
    data_points.append("31.567624,6.115178"),
    data_points.append("31.566655,6.119599"),
    data_points.append("31.569216,6.126642"),
    data_points.append("31.560634,6.134106"),
    data_points.append("31.561220,6.139456"),
    data_points.append("31.565786,6.144600"),
    data_points.append("31.564173,6.149063"),
    data_points.append("31.559706,6.155832"),
    data_points.append("31.561659,6.157912"),
    data_points.append("31.551080,6.178001"),
    data_points.append("31.554375,6.185816"),
    data_points.append("31.552682,6.187823"),
    data_points.append("31.547542,6.184459"),
    data_points.append("31.545643,6.186336"),
    data_points.append("31.548955,6.189526"),
    data_points.append("31.551265,6.195575"),
    data_points.append("31.555115,6.200500"),
    data_points.append("31.553453,6.203028"),
    data_points.append("31.545968,6.208479"),
    data_points.append("31.544613,6.212637"),
    data_points.append("31.546354,6.218869"),
    data_points.append("31.539897,6.225732"),
    data_points.append("31.530817,6.228450"),
    data_points.append("31.526403,6.230256"),
    data_points.append("31.526784,6.232209"),
    data_points.append("31.533802,6.237718"),
    data_points.append("31.533105,6.240054"),
    data_points.append("31.527798,6.238985"),
    data_points.append("31.522298,6.246182"),
    data_points.append("31.523757,6.248550"),
    data_points.append("31.533074,6.250450"),
    data_points.append("31.535305,6.253922"),
    data_points.append("31.534339,6.255746"),
    data_points.append("31.525447,6.260548"),
    data_points.append("31.519064,6.260203"),
    data_points.append("31.517240,6.263189"),
    data_points.append("31.518603,6.266154"),
    data_points.append("31.521468,6.267508"),
    data_points.append("31.521962,6.269342"),
    data_points.append("31.502730,6.286418"),
    data_points.append("31.499872,6.285141"),
    data_points.append("31.498287,6.278993"),
    data_points.append("31.495101,6.279995"),
    data_points.append("31.489918,6.284442"),
    data_points.append("31.489212,6.288187"),
    data_points.append("31.493866,6.299692"),
    data_points.append("31.491728,6.303940"),
    data_points.append("31.485488,6.306092"),
    data_points.append("31.484213,6.309420"),
    data_points.append("31.484962,6.313713"),
    data_points.append("31.482612,6.317008"),
    data_points.append("31.485732,6.327516"),
    data_points.append("31.483770,6.330206"),
    data_points.append("31.480884,6.331454"),
    data_points.append("31.482887,6.338355"),
    data_points.append("31.481101,6.342597"),
    data_points.append("31.477619,6.342329"),
    data_points.append("31.476880,6.340049"),
    data_points.append("31.476891,6.336818"),
    data_points.append("31.474509,6.337138"),
    data_points.append("31.471891,6.340518"),
    data_points.append("31.466243,6.343699"),
    data_points.append("31.464074,6.351082"),
    data_points.append("31.467697,6.361998"),
    data_points.append("31.467167,6.365439"),
    data_points.append("31.461622,6.369086"),
    data_points.append("31.443241,6.380571"),
    data_points.append("31.438319,6.380347"),
    data_points.append("31.432290,6.377214"),
    data_points.append("31.430434,6.378632"),
    data_points.append("31.434039,6.382065"),
    data_points.append("31.434833,6.385999"),
    data_points.append("31.433478,6.390061"),
    data_points.append("31.430849,6.392972"),
    data_points.append("31.425982,6.396063"),
    data_points.append("31.425478,6.398750"),
    data_points.append("31.425800,6.403089"),
    data_points.append("31.424791,6.403206"),
    data_points.append("31.422398,6.401159"),
    data_points.append("31.419780,6.401841"),
    data_points.append("31.418632,6.404997"),
    data_points.append("31.423056,6.416546"),
    data_points.append("31.420897,6.425261"),
    data_points.append("31.417506,6.430888"),
    data_points.append("31.420845,6.436590"),
    data_points.append("31.416082,6.439137"),
    data_points.append("31.414902,6.442165"),
    data_points.append("31.415758,6.461591"),
    data_points.append("31.417818,6.462391"),
    data_points.append("31.419359,6.464919"),
    data_points.append("31.419985,6.469099"),
    data_points.append("31.419073,6.470826"),
    data_points.append("31.422721,6.473107"),
    data_points.append("31.424523,6.472585"),
    data_points.append("31.425844,6.472112"),
    data_points.append("31.426359,6.473093"),
    data_points.append("31.425833,6.474863"),
    data_points.append("31.426788,6.475790"),
    data_points.append("31.428805,6.475449"),
    data_points.append("31.428344,6.478306"),
    data_points.append("31.432893,6.482133"),
    data_points.append("31.435189,6.484627"),
    data_points.append("31.436734,6.484201"),
    data_points.append("31.437464,6.480950"),
    data_points.append("31.438998,6.481334"),
    data_points.append("31.439781,6.484660"),
    data_points.append("31.441154,6.486558"),
    data_points.append("31.440918,6.488072"),
    data_points.append("31.438650,6.491806"),
    data_points.append("31.437860,6.497883"),
    data_points.append("31.436830,6.500228"),
    data_points.append("31.437173,6.502765"),
    data_points.append("31.435521,6.504311"),
    data_points.append("31.431862,6.505899"),
    data_points.append("31.430413,6.513212"),
    data_points.append("31.431325,6.516037"),
    data_points.append("31.430842,6.518244"),
    data_points.append("31.428889,6.520578"),
    data_points.append("31.426486,6.526472"),
    data_points.append("31.425875,6.531049"),
    data_points.append("31.427077,6.532264"),
    data_points.append("31.428933,6.533010"),
    data_points.append("31.430650,6.536453"),
    data_points.append("31.429824,6.541079"),
    data_points.append("31.430961,6.542646"),
    data_points.append("31.432967,6.543413"),
    data_points.append("31.433664,6.545097"),
    data_points.append("31.433396,6.547218"),
    data_points.append("31.434823,6.550597"),
    data_points.append("31.434029,6.552420"),
    data_points.append("31.430907,6.554317"),
    data_points.append("31.428632,6.552921"),
    data_points.append("31.423192,6.555223"),
    data_points.append("31.422141,6.556928"),
    data_points.append("31.424158,6.560179"),
    data_points.append("31.418568,6.562449"),
    data_points.append("31.415993,6.565561"),
    data_points.append("31.412013,6.565572"),
    data_points.append("31.407646,6.565796"),
    data_points.append("31.405135,6.566819"),
    data_points.append("31.403697,6.566190"),
    data_points.append("31.402292,6.564058"),
    data_points.append("31.400951,6.564580"),
    data_points.append("31.396069,6.569438"),
    data_points.append("31.394299,6.576760"),
    data_points.append("31.392679,6.578327"),
    data_points.append("31.391638,6.582079"),
    data_points.append("31.389417,6.582868"),
    data_points.append("31.384407,6.583433"),
    data_points.append("31.383602,6.586055"),
    data_points.append("31.380190,6.586652"),
    data_points.append("31.374375,6.589253"),
    data_points.append("31.374053,6.590713"),
    data_points.append("31.374268,6.592333"),
    data_points.append("31.371124,6.597960"),
    data_points.append("31.367573,6.599026"),
    data_points.append("31.362595,6.604142"),
    data_points.append("31.362852,6.608714"),
    data_points.append("31.361683,6.611368"),
    data_points.append("31.360642,6.611219"),
    data_points.append("31.359752,6.610196"),
    data_points.append("31.357649,6.610644"),
    data_points.append("31.355889,6.611390"),
    data_points.append("31.350675,6.610953"),
    data_points.append("31.347864,6.614854"),
    data_points.append("31.339999,6.618631"),
    data_points.append("31.333165,6.630054"),
    data_points.append("31.331802,6.631429"),
    data_points.append("31.330590,6.636033"),
    data_points.append("31.327951,6.636321"),
    data_points.append("31.325966,6.638623"),
    data_points.append("31.327146,6.640840"),
    data_points.append("31.325236,6.643067"),
    data_points.append("31.325247,6.645401"),
    data_points.append("31.323369,6.645433"),
    data_points.append("31.320805,6.645007"),
    data_points.append("31.318595,6.648950"),
    data_points.append("31.316996,6.653298"),
    data_points.append("31.315333,6.656452"),
    data_points.append("31.314711,6.663411"),
    data_points.append("31.317025,6.671074"),
    data_points.append("31.319042,6.672811"),
    data_points.append("31.320694,6.675965"),
    data_points.append("31.319471,6.678704"),
    data_points.append("31.313109,6.678917"),
    data_points.append("31.310352,6.682295"),
    data_points.append("31.309279,6.686451"),
    data_points.append("31.310084,6.688433"),
    data_points.append("31.311575,6.689115"),
    data_points.append("31.313259,6.689030"),
    data_points.append("31.316104,6.692404"),
    data_points.append("31.317295,6.695505"),
    data_points.append("31.319559,6.696485"),
    data_points.append("31.320922,6.699138"),
    data_points.append("31.324269,6.702068"),
    data_points.append("31.324891,6.704412"),
    data_points.append("31.324387,6.708994"),
    data_points.append("31.321834,6.712372"),
    data_points.append("31.323068,6.716240"),
    data_points.append("31.321598,6.719415"),
    data_points.append("31.314333,6.726006"),
    data_points.append("31.314376,6.727935"),
    data_points.append("31.314945,6.730609"),
    data_points.append("31.313765,6.732122"),
    data_points.append("31.311684,6.733209"),
    data_points.append("31.309753,6.738515"),
    data_points.append("31.307972,6.739453"),
    data_points.append("31.304356,6.741584"),
    data_points.append("31.303498,6.744503"),
    data_points.append("31.299127,6.746972"),
    data_points.append("31.298776,6.749103"),
    data_points.append("31.300176,6.753492"),
    data_points.append("31.299837,6.758201"),
    data_points.append("31.300760,6.759972"),
    data_points.append("31.299719,6.764351"),
    data_points.append("31.297477,6.765619"),
    data_points.append("31.294645,6.769401"),
    data_points.append("31.295249,6.771160"),
    data_points.append("31.296663,6.771352"),
    data_points.append("31.297317,6.773142"),
    data_points.append("31.296341,6.774218"),
    data_points.append("31.294989,6.775294"),
    data_points.append("31.294656,6.781718"),
    data_points.append("31.292617,6.783363"),
    data_points.append("31.291484,6.785067"),
    data_points.append("31.291757,6.787379"),
    data_points.append("31.290401,6.790048"),
    data_points.append("31.290400,6.792764"),
    data_points.append("31.292565,6.793606"),
    data_points.append("31.293198,6.796163"),
    data_points.append("31.289829,6.798571"),
    data_points.append("31.286031,6.799754"),
    data_points.append("31.277741,6.808686"),
    data_points.append("31.267463,6.814301"),
    data_points.append("31.263794,6.814961"),
    data_points.append("31.264255,6.818615"),
    data_points.append("31.261659,6.819851"),
    data_points.append("31.259148,6.826104"),
    data_points.append("31.255232,6.828490"),
    data_points.append("31.254299,6.830652"),
    data_points.append("31.254717,6.836916"),
    data_points.append("31.250555,6.843280"),
    data_points.append("31.245049,6.847992"),
    data_points.append("31.242431,6.850719"),
    data_points.append("31.237571,6.851752"),
    data_points.append("31.233966,6.854575"),
    data_points.append("31.230639,6.854446"),
    data_points.append("31.221245,6.858670"),
    data_points.append("31.217393,6.857797"),
    data_points.append("31.213370,6.859107"),
    data_points.append("31.208188,6.855315"),
    data_points.append("31.206310,6.852609"),
    data_points.append("31.205634,6.850692"),
    data_points.append("31.201568,6.850127"),
    data_points.append("31.198843,6.850585"),
    data_points.append("31.188383,6.849052"),
    data_points.append("31.185701,6.850533"),
    data_points.append("31.184896,6.853516"),
    data_points.append("31.179371,6.853367"),
    data_points.append("31.176345,6.851897"),
    data_points.append("31.174671,6.852739"),
    data_points.append("31.169189,6.858683"),
    data_points.append("31.166786,6.859578"),
    data_points.append("31.156454,6.859461"),
    data_points.append("31.151203,6.858720"),
    data_points.append("31.143885,6.864750"),
    data_points.append("31.143271,6.868878"),
    data_points.append("31.144065,6.878294"),
    data_points.append("31.146960,6.884620"),
    data_points.append("31.147164,6.887986"),
    data_points.append("31.145250,6.892446"),
    data_points.append("31.141107,6.898018"),
    data_points.append("31.131435,6.899820"),
    data_points.append("31.127068,6.898997"),
    data_points.append("31.122513,6.898602"),
    data_points.append("31.116784,6.896781"),
    data_points.append("31.115029,6.898238"),
    data_points.append("31.113946,6.901736"),
    data_points.append("31.111640,6.903312"),
    data_points.append("31.108464,6.904249"),
    data_points.append("31.108292,6.905580"),
    data_points.append("31.108914,6.908158"),
    data_points.append("31.110008,6.909979"),
    data_points.append("31.110931,6.909798"),
    data_points.append("31.112465,6.909052"),
    data_points.append("31.113409,6.910522"),
    data_points.append("31.112859,6.911691"),
    data_points.append("31.111529,6.912660"),
    data_points.append("31.111701,6.917155"),
    data_points.append("31.114619,6.920116"),
    data_points.append("31.114694,6.922172"),
    data_points.append("31.110769,6.926427"),
    data_points.append("31.108698,6.927865"),
    data_points.append("31.109513,6.931539"),
    data_points.append("31.109363,6.934052"),
    data_points.append("31.110715,6.936352"),
    data_points.append("31.109717,6.938109"),
    data_points.append("31.106445,6.938343"),
    data_points.append("31.105895,6.941474"),
    data_points.append("31.105262,6.944552"),
    data_points.append("31.101782,6.948368"),
    data_points.append("31.099754,6.949422"),
    data_points.append("31.097565,6.952383"),
    data_points.append("31.095441,6.953586"),
    data_points.append("31.094379,6.952553"),
    data_points.append("31.094002,6.950049"),
    data_points.append("31.091835,6.949410"),
    data_points.append("31.087071,6.951987"),
    data_points.append("31.080816,6.954000"),
    data_points.append("31.078305,6.955502"),
    data_points.append("31.073252,6.955864"),
    data_points.append("31.068753,6.956749"),
    data_points.append("31.064377,6.957610"),
    data_points.append("31.062886,6.956577"),
    data_points.append("31.063025,6.954202"),
    data_points.append("31.061373,6.950475"),
    data_points.append("31.058487,6.949911"),
    data_points.append("31.051224,6.955875"),
    data_points.append("31.045484,6.958186"),
    data_points.append("31.043345,6.957456"),
    data_points.append("31.041779,6.955188"),
    data_points.append("31.038528,6.955241"),
    data_points.append("31.036758,6.955028"),
    data_points.append("31.034269,6.953473"),
    data_points.append("31.030653,6.954133"),
    data_points.append("31.027585,6.955880"),
    data_points.append("31.024484,6.956966"),
    data_points.append("31.021486,6.958844"),
    data_points.append("31.013987,6.961208"),
    data_points.append("31.008547,6.960867"),
    data_points.append("31.003574,6.962256"),
    data_points.append("31.002104,6.964311"),
    data_points.append("31.001267,6.967570"),
    data_points.append("30.995570,6.969295"),
    data_points.append("30.990474,6.973746"),
    data_points.append("30.989626,6.978283"),
    data_points.append("30.984476,6.981904"),
    data_points.append("30.979755,6.986685"),
    data_points.append("30.974176,6.987217"),
    data_points.append("30.968318,6.989400"),
    data_points.append("30.961849,6.988857"),
    data_points.append("30.955937,6.992275"),
    data_points.append("30.952654,6.992232"),
    data_points.append("30.945433,6.988611"),
    data_points.append("30.940588,6.989741"),
    data_points.append("30.936277,6.992543"),
    data_points.append("30.930097,6.992192"),
    data_points.append("30.921125,6.992340"),
    data_points.append("30.917424,6.991829"),
    data_points.append("30.914602,6.994150"),
    data_points.append("30.913808,6.996695"),
    data_points.append("30.908841,7.001104"),
    data_points.append("30.907360,7.006333"),
    data_points.append("30.904798,7.011896"),
    data_points.append("30.899762,7.017521"),
    data_points.append("30.899183,7.020566"),
    data_points.append("30.897338,7.024879"),
    data_points.append("30.892660,7.026231"),
    data_points.append("30.886384,7.023377"),
    data_points.append("30.883981,7.021120"),
    data_points.append("30.878166,7.020460"),
    data_points.append("30.873574,7.017596"),
    data_points.append("30.871664,7.018544"),
    data_points.append("30.870720,7.021100"),
    data_points.append("30.868252,7.021675"),
    data_points.append("30.864068,7.022016"),
    data_points.append("30.862126,7.025200"),
    data_points.append("30.856869,7.026393"),
    data_points.append("30.854047,7.029779"),
    data_points.append("30.852502,7.033421"),
    data_points.append("30.849305,7.036381"),
    data_points.append("30.847910,7.041428"),
    data_points.append("30.846032,7.045112"),
    data_points.append("30.845345,7.050777"),
    data_points.append("30.849894,7.061799"),
    data_points.append("30.848489,7.065504"),
    data_points.append("30.841687,7.066452"),
    data_points.append("30.837268,7.071220"),
    data_points.append("30.832891,7.071390"),
    data_points.append("30.827924,7.071443"),
    data_points.append("30.822913,7.079247"),
    data_points.append("30.822032,7.093943"),
    data_points.append("30.823389,7.103536"),
    data_points.append("30.821864,7.110363"),
    data_points.append("30.824277,7.115638"),
    data_points.append("30.822947,7.118182"),
    data_points.append("30.817282,7.118150"),
    data_points.append("30.813688,7.118618"),
    data_points.append("30.814439,7.124314"),
    data_points.append("30.812744,7.124463"),
    data_points.append("30.810824,7.116627"),
    data_points.append("30.810170,7.112668"),
    data_points.append("30.807692,7.112785"),
    data_points.append("30.807156,7.114382"),
    data_points.append("30.807199,7.118268"),
    data_points.append("30.805472,7.121760"),
    data_points.append("30.802650,7.121920"),
    data_points.append("30.801910,7.118918"),
    data_points.append("30.800569,7.120291"),
    data_points.append("30.799282,7.125582"),
    data_points.append("30.800151,7.129053"),
    data_points.append("30.802844,7.132736"),
    data_points.append("30.802093,7.135078"),
    data_points.append("30.795752,7.136984"),
    data_points.append("30.793488,7.135557"),
    data_points.append("30.792834,7.133907"),
    data_points.append("30.793446,7.130724"),
    data_points.append("30.792148,7.128275"),
    data_points.append("30.788811,7.127051"),
    data_points.append("30.786515,7.127860"),
    data_points.append("30.783575,7.130841"),
    data_points.append("30.776225,7.134449"),
    data_points.append("30.773189,7.135790"),
    data_points.append("30.771483,7.134811"),
    data_points.append("30.768522,7.131287"),
    data_points.append("30.763801,7.133693"),
    data_points.append("30.761761,7.148903"),
    data_points.append("30.758145,7.151309"),
    data_points.append("30.754326,7.152853"),
    data_points.append("30.747480,7.159872"),
    data_points.append("30.743403,7.163087"),
    data_points.append("30.735029,7.178939"),
    data_points.append("30.729160,7.181004"),
    data_points.append("30.722873,7.177523"),
    data_points.append("30.721146,7.178811"),
    data_points.append("30.726324,7.192466"),
    data_points.append("30.728695,7.198673"),
    data_points.append("30.727697,7.205142"),
    data_points.append("30.724843,7.209038"),
    data_points.append("30.714296,7.213426"),
    data_points.append("30.709555,7.216320"),
    data_points.append("30.708600,7.220077"),
    data_points.append("30.707170,7.233044"),
    data_points.append("30.707305,7.244706"),
    data_points.append("30.703802,7.249149"),
    data_points.append("30.700680,7.253449"),
    data_points.append("30.702694,7.271878"),
    data_points.append("30.699540,7.275028"),
    data_points.append("30.692638,7.277281"),
    data_points.append("30.692917,7.280729"),
    data_points.append("30.695921,7.282017"),
    data_points.append("30.696490,7.283879"),
    data_points.append("30.692212,7.290014"),
    data_points.append("30.675270,7.301018"),
    data_points.append("30.675324,7.303253"),
    data_points.append("30.677030,7.304913"),
    data_points.append("30.677491,7.307765"),
    data_points.append("30.674948,7.314139"),
    data_points.append("30.676692,7.316898"),
    data_points.append("30.677951,7.316300"),
    data_points.append("30.680728,7.318953"),
    data_points.append("30.685320,7.322050"),
    data_points.append("30.687188,7.322275"),
    data_points.append("30.690289,7.321179"),
    data_points.append("30.691480,7.321466"),
    data_points.append("30.694286,7.324436"),
    data_points.append("30.693876,7.327181"),
    data_points.append("30.692106,7.328085"),
    data_points.append("30.691968,7.329620"),
    data_points.append("30.693016,7.333493"),
    data_points.append("30.694077,7.334522"),
    data_points.append("30.696027,7.333442"),
    data_points.append("30.697561,7.332889"),
    data_points.append("30.699158,7.334658"),
    data_points.append("30.700282,7.335839"),
    data_points.append("30.700432,7.337382"),
    data_points.append("30.698619,7.338819"),
    data_points.append("30.697503,7.344895"),
    data_points.append("30.694295,7.347885"),
    data_points.append("30.691216,7.350332"),
    data_points.append("30.690358,7.354556"),
    data_points.append("30.687998,7.355397"),
    data_points.append("30.685284,7.354461"),
    data_points.append("30.681636,7.353450"),
    data_points.append("30.680231,7.354642"),
    data_points.append("30.679383,7.357738"),
    data_points.append("30.675767,7.360675"),
    data_points.append("30.674487,7.370382"),
    data_points.append("30.671558,7.371329"),
    data_points.append("30.666580,7.372404"),
    data_points.append("30.664509,7.379118"),
    data_points.append("30.659885,7.382310"),
    data_points.append("30.655647,7.385013"),
    data_points.append("30.652493,7.391024"),
    data_points.append("30.651678,7.395152"),
    data_points.append("30.647307,7.397440"),
    data_points.append("30.641900,7.398557"),
    data_points.append("30.635355,7.406090"),
    data_points.append("30.630937,7.411105"),
    data_points.append("30.631613,7.416627"),
    data_points.append("30.622431,7.412317"),
    data_points.append("30.618998,7.414732"),
    data_points.append("30.619395,7.418690"),
    data_points.append("30.621646,7.428522"),
    data_points.append("30.624649,7.434349"),
    data_points.append("30.622997,7.436253"),
    data_points.append("30.619263,7.431636"),
    data_points.append("30.618040,7.432370"),
    data_points.append("30.616785,7.439370"),
    data_points.append("30.612654,7.441125"),
    data_points.append("30.608759,7.442763"),
    data_points.append("30.606388,7.444731"),
    data_points.append("30.600358,7.441997"),
    data_points.append("30.586757,7.443995"),
    data_points.append("30.581285,7.448304"),
    data_points.append("30.580287,7.456495"),
    data_points.append("30.582207,7.461388"),
    data_points.append("30.585930,7.463101"),
    data_points.append("30.592593,7.464165"),
    data_points.append("30.595372,7.467271"),
    data_points.append("30.593688,7.472271"),
    data_points.append("30.580767,7.481704"),
    data_points.append("30.564958,7.485176"),
    data_points.append("30.559203,7.492083"),
    data_points.append("30.559986,7.498859"),
    data_points.append("30.563194,7.502061"),
    data_points.append("30.563323,7.505965"),
    data_points.append("30.559418,7.508199"),
    data_points.append("30.553860,7.510167"),
    data_points.append("30.553248,7.514156"),
    data_points.append("30.556338,7.517294"),
    data_points.append("30.561810,7.519209"),
    data_points.append("30.565426,7.518135"),
    data_points.append("30.567894,7.513774"),
    data_points.append("30.578580,7.511324"),
    data_points.append("30.584144,7.514521"),
    data_points.append("30.583972,7.517765"),
    data_points.append("30.582652,7.524392"),
    data_points.append("30.582092,7.528503"),
    data_points.append("30.584603,7.531183"),
    data_points.append("30.583841,7.537256"),
    data_points.append("30.580261,7.545003"),
    data_points.append("30.578287,7.547694"),
    data_points.append("30.577568,7.551374"),
    data_points.append("30.571021,7.560315"),
    data_points.append("30.570961,7.564452"),
    data_points.append("30.567474,7.566983"),
    data_points.append("30.563606,7.575571"),
    data_points.append("30.564189,7.584114"),
    data_points.append("30.561003,7.585528"),
    data_points.append("30.558580,7.583689"),
    data_points.append("30.555050,7.580562"),
    data_points.append("30.550018,7.580083"),
    data_points.append("30.542957,7.586430"),
    data_points.append("30.535006,7.603414"),
    data_points.append("30.535582,7.610758"),
    data_points.append("30.538941,7.619865"),
    data_points.append("30.536866,7.627739"),
    data_points.append("30.529542,7.637143"),
    data_points.append("30.525714,7.644979"),
    data_points.append("30.520221,7.646085"),
    data_points.append("30.507321,7.646884"),
    data_points.append("30.500433,7.652123"),
    data_points.append("30.499261,7.657274"),
    data_points.append("30.504285,7.664432"),
    data_points.append("30.508866,7.666774"),
    data_points.append("30.513608,7.666370"),
    data_points.append("30.520889,7.661834"),
    data_points.append("30.525563,7.661936"),
    data_points.append("30.529774,7.667005"),
    data_points.append("30.529375,7.671254"),
    data_points.append("30.525255,7.675443"),
    data_points.append("30.524554,7.680126"),
    data_points.append("30.525262,7.684507"),
    data_points.append("30.522498,7.691548"),
    data_points.append("30.523375,7.694909"),
    data_points.append("30.525340,7.698073"),
    data_points.append("30.524213,7.700040"),
    data_points.append("30.521273,7.701380"),
    data_points.append("30.520983,7.702932"),
    data_points.append("30.523365,7.705561"),
    data_points.append("30.525103,7.706922"),
    data_points.append("30.524253,7.708471"),
    data_points.append("30.521276,7.713384"),
    data_points.append("30.521912,7.716887"),
    data_points.append("30.524530,7.717876"),
    data_points.append("30.527424,7.717573"),
    data_points.append("30.528014,7.719040"),
    data_points.append("30.527316,7.723338"),
    data_points.append("30.529725,7.730285"),
    data_points.append("30.534509,7.736931"),
    data_points.append("30.534309,7.740192"),
    data_points.append("30.529037,7.749444"),
    data_points.append("30.529337,7.752465"),
    data_points.append("30.532448,7.754761"),
    data_points.append("30.539947,7.757876"),
    data_points.append("30.548075,7.759340"),
    data_points.append("30.549867,7.761615"),
    data_points.append("30.549066,7.764288"),
    data_points.append("30.543241,7.773385"),
    data_points.append("30.540132,7.783571"),
    data_points.append("30.545613,7.793576"),
    data_points.append("30.551976,7.796875"),
    data_points.append("30.558635,7.798476"),
    data_points.append("30.559823,7.800573"),
    data_points.append("30.558227,7.803853"),
    data_points.append("30.554763,7.805640"),
    data_points.append("30.533142,7.801825"),
    data_points.append("30.530536,7.803820"),
    data_points.append("30.530800,7.806200"),
    data_points.append("30.533324,7.808958"),
    data_points.append("30.535847,7.810660"),
    data_points.append("30.536813,7.813445"),
    data_points.append("30.536802,7.815401"),
    data_points.append("30.538744,7.817293"),
    data_points.append("30.547989,7.817044"),
    data_points.append("30.550687,7.818241"),
    data_points.append("30.551492,7.821536"),
    data_points.append("30.550699,7.824585"),
    data_points.append("30.547511,7.830157"),
    data_points.append("30.544510,7.832080"),
    data_points.append("30.525475,7.838794"),
    data_points.append("30.523748,7.841228"),
    data_points.append("30.522935,7.846250"),
    data_points.append("30.525642,7.858135"),
    data_points.append("30.525916,7.865506"),
    data_points.append("30.527815,7.867738"),
    data_points.append("30.531109,7.869247"),
    data_points.append("30.531399,7.871001"),
    data_points.append("30.527353,7.875307"),
    data_points.append("30.519153,7.880522"),
    data_points.append("30.513272,7.886968"),
    data_points.append("30.510839,7.892432"),
    data_points.append("30.511429,7.896183"),
    data_points.append("30.514432,7.898656"),
    data_points.append("30.520215,7.900346"),
    data_points.append("30.521352,7.903013"),
    data_points.append("30.520762,7.905489"),
    data_points.append("30.513208,7.914918"),
    data_points.append("30.506323,7.921499"),
    data_points.append("30.502082,7.924759"),
    data_points.append("30.499100,7.930911"),
    data_points.append("30.498312,7.935438"),
    data_points.append("30.496252,7.938466"),
    data_points.append("30.493634,7.939603"),
    data_points.append("30.484597,7.940823"),
    data_points.append("30.474269,7.945208"),
    data_points.append("30.468242,7.951121"),
    data_points.append("30.463299,7.959970"),
    data_points.append("30.455256,7.967340"),
    data_points.append("30.454657,7.969778"),
    data_points.append("30.456506,7.976113"),
    data_points.append("30.459593,7.980262"),
    data_points.append("30.458649,7.982472"),
    data_points.append("30.455741,7.982313"),
    data_points.append("30.450822,7.980625"),
    data_points.append("30.444465,7.977218"),
    data_points.append("30.441538,7.978187"),
    data_points.append("30.438991,7.982375"),
    data_points.append("30.441301,7.991299"),
    data_points.append("30.443040,7.992836"),
    data_points.append("30.445759,7.992496"),
    data_points.append("30.452738,7.990542"),
    data_points.append("30.454776,7.991318"),
    data_points.append("30.455388,7.993199"),
    data_points.append("30.454111,7.997810"),
    data_points.append("30.453961,7.998188"),
    data_points.append("30.444664,8.010084"),
    data_points.append("30.443949,8.012614"),
    data_points.append("30.444335,8.017926"),
    data_points.append("30.442977,8.020179"),
    data_points.append("30.430034,8.034204"),
    data_points.append("30.429186,8.037189"),
    data_points.append("30.429522,8.043015"),
    data_points.append("30.427129,8.045150"),
    data_points.append("30.421581,8.046682"),
    data_points.append("30.416324,8.048307"),
    data_points.append("30.412258,8.048584"),
    data_points.append("30.409190,8.051452"),
    data_points.append("30.407838,8.054278"),
    data_points.append("30.406737,8.060608"),
    data_points.append("30.406909,8.066362"),
    data_points.append("30.410117,8.070569"),
    data_points.append("30.413003,8.071153"),
    data_points.append("30.415245,8.072130"),
    data_points.append("30.414902,8.073500"),
    data_points.append("30.412788,8.073755"),
    data_points.append("30.408888,8.073271"),
    data_points.append("30.401870,8.075549"),
    data_points.append("30.398295,8.078133"),
    data_points.append("30.395162,8.082180"),
    data_points.append("30.393757,8.086461"),
    data_points.append("30.394218,8.090444"),
    data_points.append("30.396203,8.097656"),
    data_points.append("30.398767,8.103094"),
    data_points.append("30.399067,8.105282"),
    data_points.append("30.397908,8.107045"),
    data_points.append("30.394078,8.108309"),
    data_points.append("30.389395,8.107927"),
    data_points.append("30.376999,8.107863"),
    data_points.append("30.369474,8.106197"),
    data_points.append("30.366491,8.107302"),
    data_points.append("30.364839,8.109915"),
    data_points.append("30.364571,8.112900"),
    data_points.append("30.367103,8.119390"),
    data_points.append("30.369914,8.125264"),
    data_points.append("30.369489,8.127521"),
    data_points.append("30.366661,8.129327"),
    data_points.append("30.364311,8.128923"),
    data_points.append("30.360738,8.125588"),
    data_points.append("30.359429,8.123559"),
    data_points.append("30.359118,8.121806"),
    data_points.append("30.359633,8.120234"),
    data_points.append("30.360481,8.118577"),
    data_points.append("30.360277,8.115284"),
    data_points.append("30.357917,8.113138"),
    data_points.append("30.355900,8.110175"),
    data_points.append("30.355020,8.107456"),
    data_points.append("30.353475,8.106096"),
    data_points.append("30.350857,8.106648"),
    data_points.append("30.348840,8.108900"),
    data_points.append("30.346480,8.109187"),
    data_points.append("30.344914,8.108316"),
    data_points.append("30.344056,8.106670"),
    data_points.append("30.344056,8.104248"),
    data_points.append("30.344389,8.102071"),
    data_points.append("30.342941,8.100733"),
    data_points.append("30.336740,8.107340"),
    data_points.append("30.331099,8.128573"),
    data_points.append("30.327196,8.134187"),
    data_points.append("30.326767,8.138627"),
    data_points.append("30.327363,8.146711"),
    data_points.append("30.325013,8.151894"),
    data_points.append("30.325206,8.155601"),
    data_points.append("30.327974,8.158596"),
    data_points.append("30.329519,8.161856"),
    data_points.append("30.328478,8.164161"),
    data_points.append("30.323350,8.165000"),
    data_points.append("30.321977,8.164108"),
    data_points.append("30.320732,8.162600"),
    data_points.append("30.317910,8.162791"),
    data_points.append("30.314691,8.165616"),
    data_points.append("30.314863,8.167825"),
    data_points.append("30.316955,8.169227"),
    data_points.append("30.321316,8.184174"),
    data_points.append("30.323346,8.189446"),
    data_points.append("30.327629,8.194966"),
    data_points.append("30.328920,8.198811"),
    data_points.append("30.327973,8.201879"),
    data_points.append("30.324604,8.204651"),
    data_points.append("30.320242,8.206145"),
    data_points.append("30.319577,8.208205"),
    data_points.append("30.320682,8.211030"),
    data_points.append("30.322431,8.212633"),
    data_points.append("30.327345,8.214481"),
    data_points.append("30.338613,8.215540"),
    data_points.append("30.341145,8.217228"),
    data_points.append("30.346316,8.223562"),
    data_points.append("30.347185,8.227618"),
    data_points.append("30.346702,8.230825"),
    data_points.append("30.345103,8.233034"),
    data_points.append("30.341949,8.234775"),
    data_points.append("30.337668,8.235072"),
    data_points.append("30.328444,8.237932"),
    data_points.append("30.324324,8.237709"),
    data_points.append("30.323262,8.239015"),
    data_points.append("30.323942,8.240773"),
    data_points.append("30.330943,8.246095"),
    data_points.append("30.333786,8.249270"),
    data_points.append("30.337369,8.255187"),
    data_points.append("30.341510,8.258011"),
    data_points.append("30.349321,8.259922"),
    data_points.append("30.351617,8.261472"),
    data_points.append("30.352379,8.264190"),
    data_points.append("30.350714,8.271977"),
    data_points.append("30.348311,8.277585"),
    data_points.append("30.346133,8.280483"),
    data_points.append("30.342689,8.282989"),
    data_points.append("30.334825,8.287002"),
    data_points.append("30.334085,8.289178"),
    data_points.append("30.334045,8.294764"),
    data_points.append("30.335343,8.297408"),
    data_points.append("30.337693,8.298831"),
    data_points.append("30.342188,8.301241"),
    data_points.append("30.344205,8.301156"),
    data_points.append("30.351468,8.299287"),
    data_points.append("30.353796,8.301177"),
    data_points.append("30.354676,8.304373"),
    data_points.append("30.354740,8.306921"),
    data_points.append("30.354182,8.309034"),
    data_points.append("30.345810,8.329504"),
    data_points.append("30.346293,8.334345"),
    data_points.append("30.348160,8.337052"),
    data_points.append("30.352001,8.339653"),
    data_points.append("30.353031,8.342371"),
    data_points.append("30.350811,8.348751"),
    data_points.append("30.347989,8.351606"),
    data_points.append("30.344974,8.352487"),
    data_points.append("30.340039,8.352073"),
    data_points.append("30.338365,8.353570"),
    data_points.append("30.338687,8.355321"),
    data_points.append("30.340039,8.356627"),
    data_points.append("30.342968,8.357020"),
    data_points.append("30.344341,8.358093"),
    data_points.append("30.348809,8.364579"),
    data_points.append("30.348423,8.366214"),
    data_points.append("30.347157,8.367233"),
    data_points.append("30.344368,8.368517"),
    data_points.append("30.339411,8.372604"),
    data_points.append("30.336750,8.376436"),
    data_points.append("30.335666,8.380363"),
    data_points.append("30.335698,8.385543"),
    data_points.append("30.336631,8.388005"),
    data_points.append("30.339657,8.390489"),
    data_points.append("30.345354,8.392315"),
    data_points.append("30.355943,8.393217"),
    data_points.append("30.358400,8.394565"),
    data_points.append("30.360256,8.397452"),
    data_points.append("30.361007,8.400944"),
    data_points.append("30.360883,8.403515"),
    data_points.append("30.360046,8.406614"),
    data_points.append("30.358651,8.408843"),
    data_points.append("30.356902,8.411316"),
    data_points.append("30.357004,8.413077"),
    data_points.append("30.358235,8.414361"),
    data_points.append("30.361854,8.416587"),
    data_points.append("30.368970,8.422221"),
    data_points.append("30.372940,8.423346"),
    data_points.append("30.378380,8.424206"),
    data_points.append("30.379764,8.425522"),
    data_points.append("30.380043,8.427761"),
    data_points.append("30.379045,8.430117"),
    data_points.append("30.377156,8.432064"),
    data_points.append("30.374677,8.432988"),
    data_points.append("30.371651,8.433593"),
    data_points.append("30.361931,8.438503"),
    data_points.append("30.361362,8.440498"),
    data_points.append("30.362137,8.442548"),
    data_points.append("30.365115,8.445297"),
    data_points.append("30.371782,8.449269"),
    data_points.append("30.374901,8.449729"),
    data_points.append("30.378817,8.449984"),
    data_points.append("30.380437,8.452223"),
    data_points.append("30.380501,8.454727"),
    data_points.append("30.379492,8.457316"),
    data_points.append("30.375597,8.461529"),
    data_points.append("30.372593,8.462824"),
    data_points.append("30.368838,8.463015"),
    data_points.append("30.365748,8.461784"),
    data_points.append("30.363999,8.460044"),
    data_points.append("30.362400,8.457126"),
    data_points.append("30.359535,8.455863"),
    data_points.append("30.355780,8.456882"),
    data_points.append("30.354568,8.458941"),
    data_points.append("30.353978,8.461000"),
    data_points.append("30.352140,8.464297"),
    data_points.append("30.351979,8.467099"),
    data_points.append("30.353771,8.469625"),
    data_points.append("30.360313,8.473161"),
    data_points.append("30.364765,8.474286"),
    data_points.append("30.364883,8.476037"),
    data_points.append("30.362233,8.477406"),
    data_points.append("30.353330,8.480244"),
    data_points.append("30.344712,8.485485"),
    data_points.append("30.342556,8.488690"),
    data_points.append("30.341666,8.492701"),
    data_points.append("30.342074,8.500108"),
    data_points.append("30.341302,8.504087"),
    data_points.append("30.339682,8.508565"),
    data_points.append("30.339596,8.515388"),
    data_points.append("30.338437,8.519431"),
    data_points.append("30.336474,8.521415"),
    data_points.append("30.332504,8.522603"),
    data_points.append("30.328738,8.522179"),
    data_points.append("30.319511,8.519601"),
    data_points.append("30.313406,8.520280"),
    data_points.append("30.309887,8.522243"),
    data_points.append("30.307280,8.525352"),
    data_points.append("30.305982,8.528928"),
    data_points.append("30.305746,8.538527"),
    data_points.append("30.303665,8.541031"),
    data_points.append("30.298494,8.544469"),
    data_points.append("30.297164,8.547365"),
    data_points.append("30.296424,8.551291"),
    data_points.append("30.294654,8.551471"),
    data_points.append("30.292025,8.549731"),
    data_points.append("30.282272,8.546240"),
    data_points.append("30.274869,8.546834"),
    data_points.append("30.272358,8.549529"),
    data_points.append("30.272347,8.552712"),
    data_points.append("30.275684,8.558781"),
    data_points.append("30.282304,8.562866"),
    data_points.append("30.293096,8.578565"),
    data_points.append("30.298157,8.584542"),
    data_points.append("30.300084,8.589279"),
    data_points.append("30.303077,8.595188"),
    data_points.append("30.309761,8.600513"),
    data_points.append("30.317890,8.609297"),
    data_points.append("30.321088,8.615812"),
    data_points.append("30.321828,8.622208"),
    data_points.append("30.323704,8.631742"),
    data_points.append("30.321062,8.640872"),
    data_points.append("30.318659,8.645286"),
    data_points.append("30.313121,8.652177"),
    data_points.append("30.309355,8.654224"),
    data_points.append("30.298873,8.655833"),
    data_points.append("30.283757,8.652156"),
    data_points.append("30.280410,8.653015"),
    data_points.append("30.278822,8.654882"),
    data_points.append("30.275781,8.664435"),
    data_points.append("30.269078,8.675378"),
    data_points.append("30.265305,8.681747"),
    data_points.append("30.246733,8.693711"),
    data_points.append("30.242362,8.699141"),
    data_points.append("30.238414,8.706703"),
    data_points.append("30.238307,8.710903"),
    data_points.append("30.244998,8.722979"),
    data_points.append("30.258237,8.730351"),
    data_points.append("30.264459,8.737530"),
    data_points.append("30.265403,8.742132"),
    data_points.append("30.261449,8.750002"),
    data_points.append("30.258327,8.752229"),
    data_points.append("30.254143,8.754413"),
    data_points.append("30.253328,8.756513"),
    data_points.append("30.254261,8.759090"),
    data_points.append("30.257158,8.760606"),
    data_points.append("30.257737,8.762780"),
    data_points.append("30.255602,8.765028"),
    data_points.append("30.245094,8.770040"),
    data_points.append("30.240899,8.773942"),
    data_points.append("30.239633,8.778362"),
    data_points.append("30.240749,8.784671"),
    data_points.append("30.242251,8.789782"),
    data_points.append("30.241768,8.799888"),
    data_points.append("30.243951,8.809873"),
    data_points.append("30.243307,8.812492"),
    data_points.append("30.241773,8.814305"),
    data_points.append("30.234113,8.820433"),
    data_points.append("30.232868,8.822882"),
    data_points.append("30.231960,8.833873"),
    data_points.append("30.233580,8.841199"),
    data_points.append("30.231960,8.843542"),
    data_points.append("30.216714,8.850967"),
    data_points.append("30.215620,8.853744"),
    data_points.append("30.216092,8.857476"),
    data_points.append("30.224511,8.879029"),
    data_points.append("30.224972,8.883184"),
    data_points.append("30.225659,8.887180"),
    data_points.append("30.228707,8.894559"),
    data_points.append("30.229072,8.899191"),
    data_points.append("30.227025,8.904802"),
    data_points.append("30.225931,8.911056"),
    data_points.append("30.223935,8.914162"),
    data_points.append("30.210241,8.930539"),
    data_points.append("30.209758,8.936199"),
    data_points.append("30.210960,8.938965"),
    data_points.append("30.217730,8.944603"),
    data_points.append("30.218148,8.947581"),
    data_points.append("30.216871,8.950220"),
    data_points.append("30.213094,8.955805"),
    data_points.append("30.213427,8.959122"),
    data_points.append("30.218975,8.968942"),
    data_points.append("30.226370,8.976396"),
    data_points.append("30.227636,8.979830"),
    data_points.append("30.229173,8.986364"),
    data_points.append("30.233143,8.988928"),
    data_points.append("30.236769,8.989076"),
    data_points.append("30.243944,8.987658"),
    data_points.append("30.247163,8.988432"),
    data_points.append("30.248955,8.991346"),
    data_points.append("30.248934,8.995574"),
    data_points.append("30.247833,9.002496"),
    data_points.append("30.248605,9.005876"),
    data_points.append("30.250965,9.007783"),
    data_points.append("30.254366,9.008260"),
    data_points.append("30.264753,9.009833"),
    data_points.append("30.268487,9.012281"),
    data_points.append("30.270289,9.017410"),
    data_points.append("30.270365,9.024698"),
    data_points.append("30.272208,9.032809"),
    data_points.append("30.274858,9.035447"),
    data_points.append("30.279718,9.037778"),
    data_points.append("30.284181,9.037767"),
    data_points.append("30.287260,9.036135"),
    data_points.append("30.294223,9.032066"),
    data_points.append("30.296626,9.032352"),
    data_points.append("30.297967,9.034143"),
    data_points.append("30.298171,9.037481"),
    data_points.append("30.297322,9.043673"),
    data_points.append("30.297837,9.051331"),
    data_points.append("30.299682,9.054361"),
    data_points.append("30.302997,9.058006"),
    data_points.append("30.306838,9.059828"),
    data_points.append("30.319457,9.062628"),
    data_points.append("30.323040,9.064482"),
    data_points.append("30.324606,9.066887"),
    data_points.append("30.326018,9.074658"),
    data_points.append("30.324495,9.079754"),
    data_points.append("30.321980,9.088710"),
    data_points.append("30.322345,9.093594"),
    data_points.append("30.331981,9.107499"),
    data_points.append("30.333275,9.111290"),
    data_points.append("30.336229,9.129844"),
    data_points.append("30.338053,9.132132"),
    data_points.append("30.348002,9.134987"),
    data_points.append("30.357843,9.138485"),
    data_points.append("30.362515,9.140555"),
    data_points.append("30.369400,9.142380"),
    data_points.append("30.371396,9.144626"),
    data_points.append("30.371825,9.148715"),
    data_points.append("30.371042,9.154128"),
    data_points.append("30.369972,9.162866"),
    data_points.append("30.370927,9.165980"),
    data_points.append("30.374433,9.168677"),
    data_points.append("30.382594,9.174374"),
    data_points.append("30.385008,9.176757"),
    data_points.append("30.388613,9.182370"),
    data_points.append("30.390147,9.187952"),
    data_points.append("30.391114,9.195635"),
    data_points.append("30.392659,9.203822"),
    data_points.append("30.391189,9.206237"),
    data_points.append("30.385256,9.209382"),
    data_points.append("30.378733,9.209647"),
    data_points.append("30.372403,9.211670"),
    data_points.append("30.368154,9.215091"),
    data_points.append("30.366200,9.220776"),
    data_points.append("30.366018,9.224535"),
    data_points.append("30.367606,9.228189"),
    data_points.append("30.370192,9.230731"),
    data_points.append("30.374151,9.235719"),
    data_points.append("30.375074,9.239436"),
    data_points.append("30.374924,9.242973"),
    data_points.append("30.375385,9.246584"),
    data_points.append("30.369869,9.262541"),
    data_points.append("30.370566,9.265421"),
    data_points.append("30.372647,9.274443"),
    data_points.append("30.373087,9.279271"),
    data_points.append("30.371703,9.282966"),
    data_points.append("30.368356,9.286714"),
    data_points.append("30.365244,9.288324"),
    data_points.append("30.362927,9.289033"),
    data_points.append("30.359440,9.289181"),
    data_points.append("30.343075,9.287092"),
    data_points.append("30.339363,9.289210"),
    data_points.append("30.337249,9.292651"),
    data_points.append("30.336670,9.296653"),
    data_points.append("30.339572,9.311842"),
    data_points.append("30.338832,9.315188"),
    data_points.append("30.332304,9.327771"),
    data_points.append("30.332411,9.330354"),
    data_points.append("30.334289,9.332630"),
    data_points.append("30.338087,9.333593"),
    data_points.append("30.342757,9.333110"),
    data_points.append("30.352944,9.331149"),
    data_points.append("30.355744,9.331572"),
    data_points.append("30.360593,9.334070"),
    data_points.append("30.368712,9.345993"),
    data_points.append("30.369649,9.348796"),
    data_points.append("30.372697,9.361258"),
    data_points.append("30.374879,9.364429"),
    data_points.append("30.376639,9.368187"),
    data_points.append("30.376910,9.382232"),
    data_points.append("30.379185,9.387429"),
    data_points.append("30.384941,9.392121"),
    data_points.append("30.395829,9.398614"),
    data_points.append("30.397717,9.401218"),
    data_points.append("30.399477,9.406309"),
    data_points.append("30.402343,9.421566"),
    data_points.append("30.404199,9.424434"),
    data_points.append("30.408276,9.426487"),
    data_points.append("30.412900,9.429694"),
    data_points.append("30.415754,9.432795"),
    data_points.append("30.417921,9.436468"),
    data_points.append("30.421961,9.447726"),
    data_points.append("30.423377,9.449483"),
    data_points.append("30.427615,9.452277"),
    data_points.append("30.433108,9.453335"),
    data_points.append("30.437560,9.454330"),
    data_points.append("30.442860,9.454785"),
    data_points.append("30.447069,9.454850"),
    data_points.append("30.450395,9.455654"),
    data_points.append("30.452788,9.456765"),
    data_points.append("30.462118,9.464579"),
    data_points.append("30.463953,9.467288"),
    data_points.append("30.469221,9.478093"),
    data_points.append("30.471399,9.483807"),
    data_points.append("30.473169,9.485542"),
    data_points.append("30.478918,9.489840"),
    data_points.append("30.485217,9.493763"),
    data_points.append("30.488768,9.495551"),
    data_points.append("30.498252,9.498094"),
    data_points.append("30.500720,9.499311"),
    data_points.append("30.502104,9.501533"),
    data_points.append("30.501364,9.503766"),
    data_points.append("30.501412,9.509826"),
    data_points.append("30.500049,9.514852"),
    data_points.append("30.500532,9.517746"),
    data_points.append("30.503085,9.519090"),
    data_points.append("30.505982,9.518889"),
    data_points.append("30.512344,9.516381"),
    data_points.append("30.521940,9.514321"),
    data_points.append("30.530491,9.513474"),
    data_points.append("30.542719,9.509719"),
    data_points.append("30.546441,9.508915"),
    data_points.append("30.556656,9.502743"),
    data_points.append("30.560923,9.501003"),
    data_points.append("30.565687,9.502495"),
    data_points.append("30.573127,9.504511"),
    data_points.append("30.581321,9.505072"),
    data_points.append("30.590647,9.504623"),
    data_points.append("30.599670,9.506432"),
    data_points.append("30.602609,9.506165"),
    data_points.append("30.625423,9.498376"),
    data_points.append("30.632822,9.498117"),
    data_points.append("30.644298,9.497770"),
    data_points.append("30.651358,9.498870"),
    data_points.append("30.660864,9.498627"),
    data_points.append("30.670871,9.497252"),
    data_points.append("30.676944,9.498141"),
    data_points.append("30.689802,9.497984"),
    data_points.append("30.697358,9.496366"),
    data_points.append("30.702079,9.493858"),
    data_points.append("30.706102,9.490398"),
    data_points.append("30.716410,9.480103"),
    data_points.append("30.722568,9.476061"),
    data_points.append("30.739079,9.465525"),
    data_points.append("30.741611,9.465059"),
    data_points.append("30.748397,9.468077"),
    data_points.append("30.749406,9.470299"),
    data_points.append("30.750307,9.474246"),
    data_points.append("30.751895,9.475823"),
    data_points.append("30.754545,9.476035"),
    data_points.append("30.761873,9.473421"),
    data_points.append("30.772975,9.466159"),
    data_points.append("30.778411,9.464114"),
    data_points.append("30.780889,9.463257"),
    data_points.append("30.788228,9.457341"),
    data_points.append("30.797466,9.455023"),
    data_points.append("30.808173,9.458388"),
    data_points.append("30.817003,9.460113"),
    data_points.append("30.839029,9.452779"),
    data_points.append("30.869485,9.459964"),
    data_points.append("30.881442,9.460601"),
    data_points.append("30.893682,9.464493"),
    data_points.append("30.901063,9.463805"),
    data_points.append("30.909068,9.461154"),
    data_points.append("30.914046,9.461641"),
    data_points.append("30.917275,9.464202"),
    data_points.append("30.918660,9.467991"),
    data_points.append("30.918762,9.474410"),
    data_points.append("30.920361,9.477712"),
    data_points.append("30.922571,9.479077"),
    data_points.append("30.936632,9.485049"),
    data_points.append("30.940205,9.485324"),
    data_points.append("30.944379,9.483927"),
    data_points.append("30.952222,9.478869"),
    data_points.append("30.957576,9.477102"),
    data_points.append("30.967339,9.475388"),
    data_points.append("30.973412,9.473769"),
    data_points.append("30.977843,9.473875"),
    data_points.append("30.985148,9.475788"),
    data_points.append("30.994546,9.476772"),
    data_points.append("31.018449,9.470735"),
    data_points.append("31.040010,9.466786"),
    data_points.append("31.044473,9.464045"),
    data_points.append("31.052905,9.456313"),
    data_points.append("31.055716,9.455784"),
    data_points.append("31.063451,9.456578"),
    data_points.append("31.069899,9.455319"),
    data_points.append("31.075585,9.452853"),
    data_points.append("31.085927,9.445118"),
    data_points.append("31.101677,9.438186"),
    data_points.append("31.114997,9.434261"),
    data_points.append("31.125843,9.433027"),
    data_points.append("31.140217,9.425123"),
    data_points.append("31.152175,9.416555"),
    data_points.append("31.163966,9.413824"),
    data_points.append("31.175210,9.416184"),
    data_points.append("31.189957,9.414246"),
    data_points.append("31.210279,9.406302"),
    data_points.append("31.229986,9.402457"),
    data_points.append("31.245720,9.398168"),
    data_points.append("31.268033,9.388892"),
    data_points.append("31.275232,9.389019"),
    data_points.append("31.293743,9.384337"),
    data_points.append("31.321784,9.375392"),
    data_points.append("31.332716,9.375280"),
    data_points.append("31.347781,9.371368"),
    data_points.append("31.355059,9.366341"),
    data_points.append("31.362089,9.358888"),
    data_points.append("31.370471,9.354269"),
    data_points.append("31.389365,9.347350"),
    data_points.append("31.399935,9.344653"),
    data_points.append("31.421058,9.336760"),
    data_points.append("31.437626,9.335360"),
    data_points.append("31.459899,9.332787"),
    data_points.append("31.479558,9.341156"),
    data_points.append("31.485790,9.346797"),
    data_points.append("31.490169,9.354148"),
    data_points.append("31.498009,9.358594"),
    data_points.append("31.508106,9.360377"),
    data_points.append("31.520513,9.363388"),
    data_points.append("31.529095,9.365711"),
    data_points.append("31.535086,9.367105"),
    data_points.append("31.545939,9.371334"),
    data_points.append("31.549378,9.375249"),
    data_points.append("31.552980,9.377440"),
    data_points.append("31.560799,9.380106"),
    data_points.append("31.567649,9.390183"),
    data_points.append("31.571547,9.394159"),
    data_points.append("31.578160,9.397636"),
    data_points.append("31.590109,9.407799"),
    data_points.append("31.594235,9.410989"),
    data_points.append("31.607873,9.429752"),
    data_points.append("31.614705,9.444489"),
    data_points.append("31.617206,9.448577"),
    data_points.append("31.619809,9.455622"),
    data_points.append("31.621900,9.457787"),
    data_points.append("31.623960,9.459681"),
    data_points.append("31.630183,9.464232"),
    data_points.append("31.636003,9.474104"),
    data_points.append("31.639442,9.478269"),
    data_points.append("31.645149,9.485491"),
    data_points.append("31.647052,9.489664"),
    data_points.append("31.650447,9.498992"),
    data_points.append("31.653588,9.505883"),
    data_points.append("31.653847,9.512255"),
    data_points.append("31.651191,9.522428"),
    data_points.append("31.644636,9.534978"),
    data_points.append("31.639954,9.556670"),
    data_points.append("31.644758,9.572383"),
    data_points.append("31.658424,9.584238"),
    data_points.append("31.671976,9.602623"),
    data_points.append("31.684654,9.618183"),
    data_points.append("31.694402,9.622709"),
    data_points.append("31.705684,9.624833"),
    data_points.append("31.721756,9.643494"),
    data_points.append("31.737614,9.656499"),
    data_points.append("31.757655,9.661290"),
    data_points.append("31.779750,9.667700"),
    data_points.append("31.786465,9.670562"),
    data_points.append("31.829673,9.678907"),
    data_points.append("31.847079,9.691867"),
    data_points.append("31.860421,9.703644"),
    data_points.append("31.889626,9.722160"),
    data_points.append("31.902283,9.726477"),
    data_points.append("31.909646,9.734351"),
    data_points.append("31.932928,9.746808"),
    data_points.append("31.942970,9.748719"),
    data_points.append("31.965882,9.754955"),
    data_points.append("31.976259,9.764426"),
    data_points.append("31.990738,9.777507"),
    data_points.append("31.997052,9.782919"),
    data_points.append("32.001444,9.790492"),
    data_points.append("32.012465,9.797663"),
    data_points.append("32.022370,9.813981"),
    data_points.append("32.027198,9.818738"),
    data_points.append("32.036311,9.839386"),
    data_points.append("32.063353,9.860971"),
    data_points.append("32.073614,9.861469"),
    data_points.append("32.083226,9.864472"),
    data_points.append("32.097436,9.866673"),
    data_points.append("32.106620,9.874236"),
    data_points.append("32.117336,9.880422"),
    data_points.append("32.133887,9.902941"),
    data_points.append("32.144517,9.910529"),
    data_points.append("32.163904,9.944172"),
    data_points.append("32.169443,9.950142"),
    data_points.append("32.172393,9.960703"),
    data_points.append("32.176007,9.966292"),
    data_points.append("32.184989,9.976383"),
    data_points.append("32.192450,9.994682"),
    data_points.append("32.201246,10.003277"),
    data_points.append("32.211312,10.008377"),
    data_points.append("32.221601,10.018096"),
    data_points.append("32.231845,10.022492"),
    data_points.append("32.237310,10.034007"),
    data_points.append("32.241372,10.040548"),
    data_points.append("32.243280,10.060862"),
    data_points.append("32.251379,10.071324"),
    data_points.append("32.267604,10.086510"),
    data_points.append("32.272696,10.091203"),
    data_points.append("32.278287,10.100968"),
    data_points.append("32.289584,10.127175"),
    data_points.append("32.299018,10.146604"),
    data_points.append("32.285401,10.213234"),
    data_points.append("32.279169,10.230266"),
    data_points.append("32.262709,10.256331"),
    data_points.append("32.263822,10.279023"),
    data_points.append("32.261248,10.294554"),
    data_points.append("32.264208,10.331939"),
    data_points.append("32.250317,10.356809"),
    data_points.append("32.252164,10.382645"),
    data_points.append("32.256748,10.397041"),
    data_points.append("32.251064,10.413507"),
    data_points.append("32.243864,10.426506"),
    data_points.append("32.230206,10.436303"),
    data_points.append("32.201963,10.434258"),
    data_points.append("32.181523,10.429202"),
    data_points.append("32.160717,10.429055"),
    data_points.append("32.130663,10.445973"),
    data_points.append("32.123432,10.466177"),
    data_points.append("32.123425,10.499374"),
    data_points.append("32.123078,10.515494"),
    data_points.append("32.130381,10.544151"),
    data_points.append("32.139138,10.548820"),
    data_points.append("32.151653,10.571207"),
    data_points.append("32.161076,10.577882"),
    data_points.append("32.173819,10.597724"),
    data_points.append("32.181355,10.606328"),
    data_points.append("32.198543,10.615430"),
    data_points.append("32.214273,10.626693"),
    data_points.append("32.242206,10.645216"),
    data_points.append("32.257790,10.656850"),
    data_points.append("32.264005,10.666293"),
    data_points.append("32.288681,10.703216"),
    data_points.append("32.311520,10.721621"),
    data_points.append("32.324411,10.740780"),
    data_points.append("32.337337,10.769568"),
    data_points.append("32.353549,10.787728"),
    data_points.append("32.359056,10.796625"),
    data_points.append("32.388625,10.798754"),
    data_points.append("32.408288,10.808194"),
    data_points.append("32.445350,10.819296"),
    data_points.append("32.457736,10.832389"),
    data_points.append("32.474526,10.842977"),
    data_points.append("32.489444,10.871386"),
    data_points.append("32.511953,10.894797"),
    data_points.append("32.523729,10.917918"),
    data_points.append("32.528765,10.931513"),
    data_points.append("32.544576,10.948015"),
    data_points.append("32.551078,10.948950"),
    data_points.append("32.560399,10.945346"),
    data_points.append("32.568703,10.949903"),
    data_points.append("32.574583,10.960613"),
    data_points.append("32.581753,10.968050"),
    data_points.append("32.595010,10.974068"),
    data_points.append("32.599159,10.976767"),
    data_points.append("32.602761,10.977810"),
    data_points.append("32.615806,10.976972"),
    data_points.append("32.630281,10.981695"),
    data_points.append("32.664648,11.017636"),
    data_points.append("32.665168,11.028290"),
    data_points.append("32.665020,11.059441"),
    data_points.append("32.660114,11.113869"),
    data_points.append("32.665553,11.130857"),
    data_points.append("32.662232,11.149072"),
    data_points.append("32.663541,11.200124"),
    data_points.append("32.655924,11.221475"),
    data_points.append("32.660851,11.231624"),
    data_points.append("32.652837,11.258318"),
    data_points.append("32.651893,11.270105"),
    data_points.append("32.639330,11.294918"),
    data_points.append("32.648863,11.313664"),
    data_points.append("32.663411,11.354389"),
    data_points.append("32.679534,11.391499"),
    data_points.append("32.680159,11.408477"),
    data_points.append("32.687048,11.432584"),
    data_points.append("32.693748,11.462718"),
    data_points.append("32.695311,11.494085"),
    data_points.append("32.700008,11.514856"),
    data_points.append("32.705366,11.536367"),
    data_points.append("32.709651,11.564258"),
    data_points.append("32.723294,11.583663"),
    data_points.append("32.736749,11.609741"),
    data_points.append("32.746420,11.639637"),
    data_points.append("32.764128,11.654368"),
    data_points.append("32.786554,11.714062"),
    data_points.append("32.784477,11.746811"),
    data_points.append("32.785335,11.761410"),
    data_points.append("32.763951,11.813735"),
    data_points.append("32.749953,11.833337"),
    data_points.append("32.750541,11.848197"),
    data_points.append("32.743093,11.870861"),
    data_points.append("32.736596,11.882262"),
    data_points.append("32.738640,11.914093"),
    data_points.append("32.745558,11.951209"),
    data_points.append("32.757517,11.982842"),
    data_points.append("32.757968,12.015409"),
    data_points.append("32.757418,12.031146"),
    data_points.append("32.750883,12.049262"),
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
