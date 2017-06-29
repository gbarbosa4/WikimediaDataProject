import simplekml
import json
from polycircles import polycircles
import time
from subprocess import call

value_separation = 0.044
radius = 2500
vertices = 200
multiplier = 100.0

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

        if extra == "medals":
            radius = 800
            vertices = 100
            multiplier = 60.0

        point_first = self.kml_var.newpoint(name=str(description[0]))
        point_second = self.kml_var.newpoint(name=str(description[2]))
        point_third = self.kml_var.newpoint(name=str(description[4]))

        pointer_first = self.generatePointer(point_first, description[1], coordinates, 'first')
        pointer_second = self.generatePointer(point_second, description[3], coordinates, 'second')
        pointer_third = self.generatePointer(point_third, description[5], coordinates, 'third')

        coord_to_kml_dict["first"] = pointer_first
        coord_to_kml_dict["second"] = pointer_second
        coord_to_kml_dict["third"] = pointer_third

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

        print(value)
        if flag == 'first':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(float(coordinates['lng']), float(coordinates['lat']), multiplier*120.0)]
        elif flag == 'second':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(float(coordinates['lng'])-float(value_separation), float(coordinates['lat'])-float(value_separation), multiplier*90.0)]
        elif flag == 'third':
            point.style.labelstyle.color = simplekml.Color.red
            point.coords = [(float(coordinates['lng'])+float(value_separation), float(coordinates['lat'])+float(value_separation), multiplier*60.0)]

        return point.coords

    def newCylinder(self, name, description, coordinates, extra):
        print ("newCylinder")
        coord_to_kml_dict = {}
        shape_polycircle_max = self.kml_var.newmultigeometry(name=name)

        coords_first = self.generateCylinder(shape_polycircle_max, description[1], coordinates, 'first')
        coords_second = self.generateCylinder(shape_polycircle_max, description[3], coordinates, 'second')
        coords_third =self.generateCylinder(shape_polycircle_max, description[5], coordinates, 'third')

        coord_to_kml_dict["first"] = coords_first
        coord_to_kml_dict["second"] = coords_second
        coord_to_kml_dict["third"] = coords_third

        if extra:
            print ('There is extra !')

        return coord_to_kml_dict

    def generateCylinder(self, shape, value, coordinates, flag):
        print("generateCylinder")
        latitude = coordinates['lat']
        longitude = coordinates['lng']
        if "," in value:
            value = value.replace(",",".")
            value = int(float(value))
        else:
            value = int(value)
        value = 120.0
        if flag == "second":
            latitude = latitude - float(value_separation)
            longitude = longitude - float(value_separation)
            value = 90.0
        elif flag == "third":
            latitude = latitude + float(value_separation)
            longitude = longitude + float(value_separation)
            value = 60.0

        polycircle = polycircles.Polycircle(latitude,longitude,radius,vertices)

        latloncircle = polycircle.to_lon_lat()
        latlonaltcircle = []
        polygon_circle = []

        multiplier = 100.0

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

        return coord_to_kml

    def addColor(self, polygon, flag):
        if flag == 'first':
            polygon.style.polystyle.color = simplekml.Color.blue
            polygon.style.linestyle.color = simplekml.Color.blue
        elif flag =='second':
            polygon.style.polystyle.color = simplekml.Color.red
            polygon.style.linestyle.color = simplekml.Color.red
        elif flag =='third':
            polygon.style.polystyle.color = simplekml.Color.red
            polygon.style.linestyle.color = simplekml.Color.red
