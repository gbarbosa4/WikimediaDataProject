import simplekml
import json
from polycircles import polycircles
import time
from subprocess import call

class CylindersKml(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.kml_var = simplekml.Kml()

    def makeKML(self):
        print ("makeKML")
        print("--- ",self.data['coordinates'])
        list_to_return = []
        pointer = self.parseData_pointer()
        cylinder = self.parseData_cylinder()
        list_to_return.append(pointer)
        list_to_return.append(cylinder)

        return list_to_return

    def parseData_pointer(self):
        print ("parseData")
        return self.newPointer(self.data['name'], self.data['description'], self.data['coordinates'], self.data['extra'])

    def parseData_cylinder(self):
        print ("parseData")
        return self.newCylinder(self.data['name'], self.data['description'], self.data['coordinates'], self.data['extra'])

    def newPointer(self, name, description, coordinates, extra):
        coord_to_kml_dict = {}

        point_nations = self.kml_var.newpoint(name=str(description[0]))
        point_athletes = self.kml_var.newpoint(name=str(description[1]))
        point_events = self.kml_var.newpoint(name=str(description[2]))

        pointer_nations = self.generatePointer(point_nations, description[0], coordinates, 'nations')
        pointer_athletes = self.generatePointer(point_athletes, description[1], coordinates, 'athletes')
        pointer_events = self.generatePointer(point_events, description[2], coordinates, 'events')

        coord_to_kml_dict["nations"] = pointer_nations
        coord_to_kml_dict["athletes"] = pointer_athletes
        coord_to_kml_dict["events"] = pointer_events

        if extra:
            print ('There is extra !')

        return coord_to_kml_dict

    def generatePointer(self, point, value, coordinates, flag):
        print("generatePointer")
        point.altitudemode = 'relativeToGround'
        point.gxballoonvisibility = 0
        point.style.iconstyle.scale = 0
        point.style.labelstyle.scale = 1
        point.style.balloonstyle.displaymode = 'hide'

        latitude = coordinates['lat']
        longitude = coordinates['lng']

        if "," in value:
            value = value.replace(",",".")
            value = int(float(value))
        else:
            value = int(value)

        multiplier = 60.0

        if flag == 'nations':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(float(coordinates['lng']), float(coordinates['lat']), multiplier*value)]
        elif flag == 'athletes':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(float(coordinates['lng'])+0.025, float(coordinates['lat'])+0.025, multiplier*value)]
        elif flag == 'events':
            point.style.labelstyle.color = simplekml.Color.red
            point.coords = [(float(coordinates['lng'])-0.025, float(coordinates['lat'])-0.025, multiplier*value)]

        return point.coords

    def newCylinder(self, name, description, coordinates, extra):
        print ("newCylinder")
        coord_to_kml_dict = {}
        shape_polycircle_max = self.kml_var.newmultigeometry(name=name)

        coords_nations = self.generateCylinder(shape_polycircle_max, description[0], coordinates, 'nations')
        coords_athletes = self.generateCylinder(shape_polycircle_max, description[1], coordinates, 'athletes')
        coords_events =self.generateCylinder(shape_polycircle_max, description[2], coordinates, 'events')

        coord_to_kml_dict["nations"] = coords_nations
        coord_to_kml_dict["athletes"] = coords_athletes
        coord_to_kml_dict["events"] = coords_events

        if extra:
            print ('There is extra !')

        return coord_to_kml_dict

    def generateCylinder(self, shape, value, coordinates, flag):
        print("generateCylinder")
        latitude = coordinates['lat']
        longitude = coordinates['lng']
        radius = 1000
        vertices = 200
        if "," in value:
            value = value.replace(",",".")
            value = int(float(value))
        else:
            value = int(value)

        if flag == "athletes":
            latitude = latitude + float(0.025)
            longitude = longitude + float(0.025)
        elif flag == "events":
            latitude = latitude - float(0.025)
            longitude = longitude - float(0.025)

        polycircle = polycircles.Polycircle(latitude,longitude,radius,vertices)

        latloncircle = polycircle.to_lon_lat()
        latlonaltcircle = []
        polygon_circle = []

        multiplier = 60.0

        # 'Pal' cap a dalt i cercle al final del pal (a dalt de tot)
        for element in latloncircle:
            tup = (element[0], element[1], (value * multiplier) + 10.0,)
            latlonaltcircle.append(tup)

        # Cilindre (interior / exterior)
        for element in latloncircle:
            tup = (element[0], element[1], value * multiplier,)
            latlonaltcircle.append(tup)

            tup = (element[0], element[1], 0,)
            latlonaltcircle.append(tup)

        #Un altre cilindre (interior / exterior ?)
        for element in latloncircle:
            tup = (element[0], element[1], 0,)
            latlonaltcircle.append(tup)

            tup = (element[0], element[1], value * multiplier,)
            latlonaltcircle.append(tup)

        for element in latloncircle:
            tup = (element[0], element[1], 0,)
            latlonaltcircle.append(tup)

        pol = shape.newpolygon()
        pol.outerboundaryis = latlonaltcircle

        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        pol.extrude = 5
        pol.style.linestyle.width = 5000

        polygon_circle.append(polycircle)

        #latlonaltcircle = []

        # Cyrcle (tapadera del cilindre) de dalt de tot (interior i exterior)
        for element in latloncircle:
            tup = (element[0], element[1], (value * multiplier) + 20.0,)
            latlonaltcircle.append(tup)

        pol = shape.newpolygon()

        pol.outerboundaryis = latlonaltcircle

        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        pol.extrude = 5
        self.addColor(pol, flag)

        pol.style.linestyle.width = 5000

        polygon_circle.append(polycircle)

        coord_to_kml = ""

        for element in latlonaltcircle:
            if coord_to_kml == str(""):
                coord_to_kml = coord_to_kml + str(element[0]) + "," + str(element[1])  + "," + str(element[2])

            else:
                coord_to_kml = coord_to_kml + " " + str(element[0])  + "," + str(element[1])  + "," + str(element[2])
        #print (coord_to_kml)
        return coord_to_kml

    def addColor(self, polygon, flag):
        if flag == 'nations':
            polygon.style.polystyle.color = simplekml.Color.blue
            polygon.style.linestyle.color = simplekml.Color.blue
        elif flag =='athletes':
            polygon.style.polystyle.color = simplekml.Color.red
            polygon.style.linestyle.color = simplekml.Color.red
        elif flag =='events':
            polygon.style.polystyle.color = simplekml.Color.red
            polygon.style.linestyle.color = simplekml.Color.red
