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
kml_file_name_river_tour= "kml_file_tour_experience"
kml_file_name_river_line_track = "kml_file_line_track_experience"
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
		sendKML_ToGalaxy(kml_file, kml_name)

	elif use_case == "Premier League Stadiums":
		kml_file = generator_kml.generateKML_premierLeague_Stadiums()
		write_FlyTo_andSend(kml_file.name)
		sendKML_ToGalaxy(kml_file, kml_name)
		time.sleep(10)
		start_tour_premier_league()

	elif use_case == "Longest Rivers":
		kml_file = generator_kml.generateKML_Longest_Rivers()
		sendKML_ToGalaxy(kml_file, kml_name)

	elif use_case == "Tour Experience":
		kml_file = generator_kml.generateKML_Tour_Experience(data_set)

		ip_galaxy_master = get_galaxy_ip()
		ip_server = get_server_ip()

		sendKML_ToGalaxy(kml_file, kml_name)
		time.sleep(5.0)

		file = open("kml_tmp/query.txt", 'w+')
		file.write("playtour=Tour Experience")
		file.close()

		os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
		print ("Query file send!!")

	elif use_case == "Line Track Experience":
		kml_file = generator_kml.generateKML_Line_Track_Experience(data_set)
        
		ip_galaxy_master = get_galaxy_ip()
		ip_server = get_server_ip()

		sendKML_ToGalaxy(kml_file, kml_name)
		time.sleep(5.0)

		file = open("kml_tmp/query.txt", 'w+')
		file.write("playtour=Line Track Experience")
		file.close()

		os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)
		print ("Query file send!!")

	elif use_case == "Spanish Airports":
		kml_file = generator_kml.generateKML_Spanish_Airports()
		sendKML_ToGalaxy(kml_file, kml_name)

	elif use_case == "Summer Olympic Games":
		kml_file = generator_kml.generateKML_Olympic_Games()
		sendKML_ToGalaxy(kml_file, kml_name)
		write_FlyTo_andSend(kml_file.name)

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

def stop_experience(request):
	print("stop experience")
	list_rivers = informationList.get_information_list("Longest_Rivers")

	ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()

	file = open("kml_tmp/query.txt", 'w+')
	file.write("exittour=true")
	file.close()

	os.system("sshpass -p 'lqgalaxy' scp " + file_query_txt_path + " lg@"+ ip_galaxy_master +":" + serverPath_query)

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers})

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

				club_name = result["clubName"]["value"]
				club_short_name = result["clubsLabel"]["value"]
				hash_stadium_club[club_name] = stadium_name

				hash_club_shield = hash_club_shield + club_name + "=" + getClubShieldImage(wikiapi.find(club_short_name)) + "|"

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

		informationList.set_information_list("Premier_League_Stadiums",clubstadium_list)
		informationList.set_information_list("Premier_League_Stadiums_aux",hash_club_shield)
		stadium_name = ""

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
					    print("equalssss")
					    club_shield_image = hash_club_shield.split("|")[i].split("=")[1]
					    i=20
					  i=i+1
					clubstadium.addClubShield(club_shield_image)

		generate_kml("Premier League Stadiums", clubstadium_selected, kml_file_name_premierLeague_stadium)

	return render(request, 'WDLG/indexPremierLeagueStadiums.html', {"clubs_list": clubs_list , "stadium_name": stadium_name, "club_shield_image": club_shield_image , "club_selected": club_selected, "hash_club_shield": hash_club_shield} )

def getStadiumByClub(club, hash_stadium_club):
    for key, value in hash_stadium_club.items():
        if key == club:
            return value

def longest_rivers_query(request):

	print ("Obtaining data longest rivers ...\n")
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

		generate_kml("Longest Rivers", list_rivers, kml_file_name_longest_rivers)

	else:
		list_rivers = informationList.get_information_list("Longest_Rivers")
		river_name = ""
		data_points = []

		for key,value in request.POST.items():
				if key == "river_name":
						river_name = value

		data_points = get_river_dynamic_points(river_name)

		informationList.set_information_list("Data_Points",data_points)
		print(river_name+" Points saved.")

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers} )

def get_river_dynamic_points(river_name):
    data_points = []

    with open("static/river_points/"+str(river_name)+".txt", 'r+') as file:
        for line in file:
            data_points.append(line.splitlines())

    return data_points

def tour_experience(request):
	river_name = ""

	for key,value in request.POST.items():
		if key == "river_name":
			river_name = value

	data_points = informationList.get_information_list("Data_Points")
	list_rivers = informationList.get_information_list("Longest_Rivers")
	print("rrrr ",river_name)

	generate_kml("Tour Experience", data_points, kml_file_name_river_tour+"_"+river_name)

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers})

def line_track_experience(request):
	river_name = ""

	for key,value in request.POST.items():
		if key == "river_name":
			river_name = value

	data_points = informationList.get_information_list("Data_Points")
	list_rivers = informationList.get_information_list("Longest_Rivers")

	generate_kml("Line Track Experience", data_points, kml_file_name_river_line_track+"_"+river_name)

	return render(request, 'WDLG/indexLongestRivers.html', {"list_rivers": list_rivers})

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
