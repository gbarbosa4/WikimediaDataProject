import simplekml
import json
from polycircles import polycircles
import time
from subprocess import call

value_separation = 0.075
value_lat_center_medal = 0.0305
value_lng_center_medal = 0.0570

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
            point_golden = self.kml_var.newpoint(name=str(description[0])+" golden medals")
            point_silver = self.kml_var.newpoint(name=str(description[0])+" silver medals")
            point_bronze = self.kml_var.newpoint(name=str(description[0])+" bronze medals")

            pointer_golden = self.generatePointer(point_golden, description[1], coordinates, 'golden')
            pointer_silver = self.generatePointer(point_silver, description[2], coordinates, 'silver')
            pointer_bronze = self.generatePointer(point_bronze, description[3], coordinates, 'bronze')

            coord_to_kml_dict["golden"] = pointer_golden
            coord_to_kml_dict["silver"] = pointer_silver
            coord_to_kml_dict["bronze"] = pointer_bronze

        elif extra == "podium":
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
        point.altitudemode = 'absolute'
        point.gxballoonvisibility = 0
        point.style.iconstyle.scale = 0
        point.style.labelstyle.scale = 1
        point.style.balloonstyle.displaymode = 'hide'

        latitude = float(coordinates['lat'])
        longitude = float(coordinates['lng'])
        multiplier = 150.0
        if "," in value:
            value = value.replace(",",".")
            value = int(float(value))
        else:
            value = int(value)

        print(value)
        print("cooooooordddd ",coordinates)

        if flag == 'first':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(longitude, latitude, multiplier*120.0)]
        elif flag == 'second':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(longitude-float(value_separation), latitude-float(value_separation), multiplier*90.0)]
        elif flag == 'third':
            point.style.labelstyle.color = simplekml.Color.red
            point.coords = [(longitude+float(value_separation), latitude+float(value_separation), multiplier*60.0)]
        if flag == 'golden':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(longitude + value_lng_center_medal, latitude - value_lat_center_medal, multiplier*value)]
        elif flag == 'silver':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(longitude + (value_lng_center_medal-0.0240), latitude - (value_lat_center_medal+0.0180), multiplier*value)]
        elif flag == 'bronze':
            point.style.labelstyle.color = simplekml.Color.red
            point.coords = [(longitude + (value_lng_center_medal+0.0240), latitude - (value_lat_center_medal-0.0180), multiplier*value)]

        return point.coords

    def newCylinder(self, name, description, coordinates, extra):
        print ("newCylinder")
        coord_to_kml_dict = {}

        if extra == "podium":
            shape_polycircle = self.kml_var.newmultigeometry(name=name)

            coords_first = self.generateCylinder(shape_polycircle, description[1], coordinates, 'first')
            coords_second = self.generateCylinder(shape_polycircle, description[3], coordinates, 'second')
            coords_third =self.generateCylinder(shape_polycircle, description[5], coordinates, 'third')

            coord_to_kml_dict["first"] = coords_first
            coord_to_kml_dict["second"] = coords_second
            coord_to_kml_dict["third"] = coords_third

        elif extra == "medals":
            shape_polycircle = self.kml_var.newmultigeometry(name=name)

            coords_golden = self.generateCylinder(shape_polycircle, description[1], coordinates, 'golden')
            coords_silver = self.generateCylinder(shape_polycircle, description[2], coordinates, 'silver')
            coords_bronze =self.generateCylinder(shape_polycircle, description[3], coordinates, 'bronze')

            coord_to_kml_dict["golden"] = coords_golden
            coord_to_kml_dict["silver"] = coords_silver
            coord_to_kml_dict["bronze"] = coords_bronze

        return coord_to_kml_dict

    def generateCylinder(self, shape, value, coordinates, flag):
        print("generateCylinder")
        latitude = coordinates['lat']
        longitude = coordinates['lng']
        radius = 4200
        vertices = 200
        multiplier = 150.0

        if "," in value:
            value = value.replace(",",".")
            value = int(float(value))
        else:
            value = int(value)

        if flag == "first":
            value = 120.0

        elif flag == "second":
            latitude = latitude - float(value_separation)
            longitude = longitude - float(value_separation)
            value = 90.0

        elif flag == "third":
            latitude = latitude + float(value_separation)
            longitude = longitude + float(value_separation)
            value = 60.0

        elif flag == "golden":
            latitude = latitude - value_lat_center_medal
            longitude = longitude + value_lng_center_medal
            radius = 1000
            vertices = 100
            print("value gold ",value)

        elif flag == "silver":
            latitude = latitude - (value_lat_center_medal+0.0180)
            longitude = longitude + (value_lng_center_medal-0.0230)
            radius = 1000
            vertices = 100
            print("value silver ",value)

        elif flag == "bronze":
            latitude = latitude - (value_lat_center_medal-0.0180)
            longitude = longitude + (value_lng_center_medal+0.0230)
            radius = 1000
            vertices = 100
            print("value bronze ",value)

        polycircle = polycircles.Polycircle(latitude,longitude,radius,vertices)

        latloncircle = polycircle.to_lon_lat()
        latlonaltcircle = []
        polygon_circle = []

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

        pol.altitudemode = simplekml.AltitudeMode.absolute
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

        pol.altitudemode = simplekml.AltitudeMode.absolute
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
