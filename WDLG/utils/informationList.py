
class InformationList(object):
    populatedCitiesList = None
    premierLeagueStadiumsList = None
    hash_club_shield = None
    olympicGamesList = None
    longest_rivers_list = None
    data_points = None

    def __init__(self):
        print("New Information List")

    def set_information_list(self,type,list):
        if type == "Olympic_Games":
            self.olympicGamesList = list
        if type == "Populated_Cities":
            self.populatedCitiesList = list
        if type == "Premier_League_Stadiums":
            self.premierLeagueStadiumsList = list
        if type == "Premier_League_Stadiums_aux":
            self.hash_club_shield = list
        if type == "Longest_Rivers":
            self.longest_rivers_list = list
        if type == "Data_Points":
            self.data_points = list

    def get_information_list(self,type):
        if type == "Olympic_Games":
            return self.olympicGamesList
        if type == "Populated_Cities":
            return self.populatedCitiesList
        if type == "Premier_League_Stadiums":
            return self.premierLeagueStadiumsList
        if type == "Premier_League_Stadiums_aux":
            return self.hash_club_shield
        if type == "Longest_Rivers":
            return self.longest_rivers_list
        if type == "Data_Points":
            return self.data_points
