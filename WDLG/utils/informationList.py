
class InformationList(object):
    olympicGamesList = None

    def __init__(self):
        print("New Information List")

    def set_information_list(self,type,list):
        if type == "Olympic_Games":
            self.olympicGamesList = list

    def get_information_list(self,type):
        if type == "Olympic_Games":
            return self.olympicGamesList
