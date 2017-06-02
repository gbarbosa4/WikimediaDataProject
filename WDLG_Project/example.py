#!/usr/bin/python

from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import os
from city import City
from river import River
from kml_generator import GeneratorKML

NUM_CITIES = 10
NUM_RIVERS = 10

cities_list = []
rivers_list = []

def menu():
	os.system('clear')
	print ("***** WIKIDATA LIQUID GALAXY PROJECT ******\n")
	print ("-> Choose one of the options")
	print ("\t1 - Most populated cities in the world.")
	print ("\t2 - European football stadiums with more capacity.")
	print ("\t3 - The longest rivers in the world.")
	print ("\tE - Exit")

def posible_options_menu(opcion_menu):

	if opcion_menu=="1":
		print ("")
		print("You have chosen option 1.")
		print("--- MOST POPULATED CITIES IN THE WORLD ---")
		print(".............................................\n")
		cities_list = populated_cities_query()
		generate_kml(cities_list)
	elif opcion_menu=="2":
		print ("")
		print("You have chosen option 2.")
		print("--- EUROPEAN FOOTBALL STADIUMS WITH MORE CAPACITY ---")
		print("......................................................\n")
	elif opcion_menu=="3":
		print ("")
		print("You have chosen option 3.")
		print("--- THE LONGEST RIVERS IN THE WORLD ---")
		print(".........................................\n")
		rivers_list = longest_rivers_query()
	elif opcion_menu=="E":
		print("EXIT")
	else:
		print ("")
		print("The chosen option doesn't exist. Please, choose a valid option")
		opcion_menu = input("\nInsert your option: ")
		posible_options_menu(opcion_menu)

def main():
	menu()
	opcion_menu = input("\nInsert your option: ")
	posible_options_menu(opcion_menu)

def populated_cities_query():

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

	print ("----- CITY INFORMATION -----")
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

	return list_cities

def longest_rivers_query():

	print ("Obtaining data ...\n")
	list_rivers = []
	rank = 1
	i = 1
	sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

	sparql.setReturnFormat(JSON)

	sparql.setQuery("""SELECT DISTINCT ?river ?riverLabel (MAX(?length) AS ?length) (SAMPLE(?image) AS ?image)
	   		(SAMPLE(?coord) AS ?coord) ?continentLabel (SAMPLE(?origin) AS ?origin) ?mouthLabel
	   		(MAX(?discharge) AS ?discharge)
			WHERE
			{
			?river wdt:P31/wdt:P279* wd:Q4022 .
			?river wdt:P2043 ?length .
			?river wdt:P18 ?image .
			?river wdt:P625 ?coord .
			?river wdt:P30 ?continent .
			?river wdt:P885 ?origin .
			?river wdt:P403 ?mouth .
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

	    mouth = result["mouthLabel"]["value"]

	    discharge = result["discharge"]["value"]

	    list_rivers.append(River(rank, river, image, length, continent, origin, mouth, discharge))
	    list_rivers[rank-1].coordinates(latitude,longitude)

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

	return list_rivers

def generate_kml(cities_list):

	generator_kml = GeneratorKML(cities_list,"kml_file_tour_city","")
	tour_city_file = generator_kml.generateFile()
	sendKML_ToGalaxy(tour_city_file)

def sendKML_ToGalaxy(kml_file):
    ip_galaxy_master = get_galaxy_ip()
	ip_server = get_server_ip()
	print("seeendddd")
    file_kmls_txt_path = "/tmp/kml/kmls.txt"
    serverPath = "/var/www/html/"
    os.system("sshpass -p 'lqgalaxy' scp " + file_kmls_txt_path + " lg@"+ ip_server +":" + serverPath)

def get_galaxy_ip():
	ip_galaxy = input("\nInsert IP Liquid Galaxy master: ")
    return ip_galaxy

def get_server_ip():
    p = subprocess.Popen(
        "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'",
        #"ifconfig eno1 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'",
        shell=True,
        stdout=subprocess.PIPE)
    ip_server = p.communicate()[0]
    return ip_server

if __name__ == "__main__":
    main()
