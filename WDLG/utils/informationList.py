
class InformationList(object):
    populatedCitiesList = None
    premierLeagueStadiumsList = None
    hash_club_shield = None
    olympicGamesList = None

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

    def get_information_list(self,type):
        if type == "Olympic_Games":
            return self.olympicGamesList
        if type == "Populated_Cities":
            return self.populatedCitiesList
        if type == "Premier_League_Stadiums":
            return self.premierLeagueStadiumsList
        if type == "Premier_League_Stadiums_aux":
            return self.hash_club_shield
