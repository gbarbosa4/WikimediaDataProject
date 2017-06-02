
class ClubStadium(object):
    stadiumName = None
    clubShortName = None
    clubName = None
    clubShieldImage = None
    clubFounded = None
    clubCoach = None
    clubCity = None
    stadiumImage = None
    stadiumCapacity = None
    latitude = None
    longitude = None

    def __init__(self, stadium_name, club_short_name, club_name, club_founded, club_coach, club_city, stadium_image, stadium_capacity):
        self.stadiumName = stadium_name
        self.clubShortName = club_short_name
        self.clubName = club_name
        self.clubFounded = club_founded
        self.clubCoach = club_coach
        self.clubCity = club_city
        self.stadiumImage = stadium_image
        self.stadiumCapacity = stadium_capacity

    def coordinates(self, longitude, latitude): #longitude E/W, latitude S/N
        self.longitude = longitude
        self.latitude = latitude

    def addClubShield(self, club_shield_image):
        self.clubShieldImage = club_shield_image
