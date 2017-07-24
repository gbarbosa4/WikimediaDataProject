
class InformationList(object):
    populatedCitiesList = None
    olympicGamesList = None

    def __init__(self):
        print("New Information List")

    def set_information_list(self,type,list):
        if type == "Olympic_Games":
            self.olympicGamesList = list
        if type == "Populated_Cities":
            self.populatedCitiesList = list

    def get_information_list(self,type):
        if type == "Olympic_Games":
            return self.olympicGamesList
        if type == "Populated_Cities":
            return self.populatedCitiesList
