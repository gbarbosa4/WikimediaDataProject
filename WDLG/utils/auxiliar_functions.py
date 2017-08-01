from .wikiapi import *

class Auxiliar_Functions(object):

    def getClubShieldImage(self,response_xml):
    	wikiapi = WikiApi({ 'locale' : 'en'})
    	response_xml = wikiapi.replace(response_xml)
    	ind_i = wikiapi.getIndex_substring("infobox",response_xml)
    	ind_f = wikiapi.getIndex_substring("scope",response_xml)
    	response_xml = response_xml[ind_i:ind_f]
    	ind_i = wikiapi.getIndex_substring("src=\"",response_xml)
    	ind_f = wikiapi.getIndex_substring("\" width",response_xml)
    	return "https:"+response_xml[ind_i+len("src=\""):ind_f]

    def getStadiumByClub(self,club, hash_stadium_club):
        for key, value in hash_stadium_club.items():
            if key == club:
                return value

    def get_river_dynamic_points(self,river_name):
        data_points = []

        with open("static/river_points/"+str(river_name)+".txt", 'r+') as file:
            for line in file:
                data_points.append(line.splitlines())

        return data_points

    def do_data_list(self,hash_data):
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

    def getCoord_byCity(self,city):
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
