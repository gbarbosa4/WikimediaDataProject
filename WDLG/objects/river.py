
class River(object):
    rank = None
    river = None
    image = None
    length = None
    continent = None
    origin = None
    mouth = None
    discharge = None
    latitude = None
    longitude = None
    latitude_orig = None
    longitude_orig = None
    latitude_mouth = None
    longitude_mouth = None

    def __init__(self, rank, river, image, length, continent, origin, mouth, discharge):
        self.rank = rank
        self.river = river
        self.image = image
        self.length = length
        self.continent = continent
        self.origin = origin
        self.mouth = mouth
        self.discharge = discharge

    def coordinates(self, latitude, longitude): #latitude S/N, longitude E/W
        self.latitude = latitude
        self.longitude = longitude

    def coordinates_origin(self, latitude_orig, longitude_orig): #latitude S/N, longitude E/W
        self.latitude_orig = latitude_orig
        self.longitude_orig = longitude_orig

    def coordinates_mouth(self, latitude_mouth, longitude_mouth): #latitude S/N, longitude E/W
        self.latitude_mouth = latitude_mouth
        self.longitude_mouth = longitude_mouth
