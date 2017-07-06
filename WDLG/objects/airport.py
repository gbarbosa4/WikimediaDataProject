
class Airport(object):
    airport = None
    image = None
    opening = None
    city = None
    latitude = None
    longitude = None

    def __init__(self, airport, image, opening, city):
        self.airport = airport
        self.image = image
        self.opening = opening
        self.city = city

    def coordinates(self, longitude, latitude): #longitude E/W, latitude S/N
        self.longitude = longitude
        self.latitude = latitude
