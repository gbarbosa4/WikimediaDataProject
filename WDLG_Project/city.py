
class City(object):
    rank = None
    city = None
    image = None
    population = None
    area = None
    density = None
    country = None
    elevation = None
    latitude = None
    longitude = None

    def __init__(self, rank, city, image, population, area, density, country, elevation):
        self.rank = rank
        self.city = city
        self.image = image
        self.population = population
        self.area = area
        self.density = density
        self.country = country
        self.elevation = elevation

    def coordinates(self, longitude, latitude): #longitude E/W, latitude S/N
        self.longitude = longitude
        self.latitude = latitude
