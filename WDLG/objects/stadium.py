
class TeamStadium(object):
    stadiumName = None
    team = None
    club_fundation = None
    coach = None
    city = None
    image = None
    capacity = None
    stadium_inaguration = None
    latitude = None
    longitude = None

    def __init__(self, stadiumName, team, club_fundation, coach, city, image, capacity, stadium_inaguration):
        self.stadiumName = stadiumName
        self.team = team
        self.club_fundation = club_fundation
        self.coach = coach
        self.city = city
        self.image = image
        self.capacity = capacity
        self.stadium_inaguration = stadium_inaguration

    def coordinates(self, longitude, latitude): #longitude E/W, latitude S/N
        self.longitude = longitude
        self.latitude = latitude
