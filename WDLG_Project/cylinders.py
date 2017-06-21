import simplekml
import json
from polycircles import polycircles
import time
from subprocess import call

class CylindersKml(object):

    def __init__(self, name, data):
        print ("New Cylinder ",data)
        self.name = name
        self.data = data
        self.kml_var = simplekml.Kml()

    def makeKML(self):
        print("makeKML")
        #current_milli_time = int(round(time.time()))
        return self.parseData()
        #self.saveKml(current_milli_time)
        #self.sendKml(current_milli_time)

    def parseData(self):
        #for element in self.data:
            #if(not element['description'][0]==None and not element['description'][1]==None):
        return self.newCylinder(self.data['name'], self.data['description'], self.data['coordinates'], self.data['extra'])
        #self.newPointer(self.data['name'], self.data['description'], self.data['coordinates'], self.data['extra'])

    def newPointer(self, name, description, coordinates, extra):
        pointer_max = self.kml_var.newpoint(name=str(description[0])+ u'\u2103')
        pointer_min = self.kml_var.newpoint(name=str(description[1])+ u'\u2103')
        self.generatePointer(pointer_max, description[0], coordinates, 'max')
        self.generatePointer(pointer_min, description[1], coordinates, 'min')

        if extra:
            print ('There is extra !')

    def generatePointer(self, point, temp, coordinates, flag):
        point.altitudemode = 'relativeToGround'
        point.gxballoonvisibility = 0
        point.style.iconstyle.scale = 0
        point.style.labelstyle.scale = 1
        point.style.balloonstyle.displaymode = 'hide'
        if flag == 'min':
            point.style.labelstyle.color = simplekml.Color.lightblue
            point.coords = [(float(coordinates['lng'])-0.025, float(coordinates['lat'])-0.025, 2200*int(temp))]
        elif flag == 'max':
            point.style.labelstyle.color = simplekml.Color.red
            point.coords = [(float(coordinates['lng']), float(coordinates['lat']), 2200*int(temp))]

    def newCylinder(self, name, description, coordinates, extra):
        print("-> newCylinder")
        shape_polycircle_max = self.kml_var.newmultigeometry(name=name+'-max')
        shape_polycircle_min = self.kml_var.newmultigeometry(name=name+'-min')
        print(shape_polycircle_min)
        coord_to_kml = self.generateCylinder(shape_polycircle_max, description[0], coordinates, 'max')
        return coord_to_kml
        #self.generateCylinder(shape_polycircle_min, description[1], coordinates, 'min')

        if extra:
            print ('There is extra !')

    def generateCylinder(self, shape, temp, coordinates, flag):
        print ("-> generateCylinder")
        polycircle = None
        if flag == 'min':
            print("lolo")
            #polycircle = polycircles.Polycircle(coordinates['lat'],coordinates['lng'],1000,100)
        elif flag == 'max':
            print(coordinates['lat']," ",type(coordinates['lat']))
        polycircle = polycircles.Polycircle(coordinates['lat'],coordinates['lng'],1000,100)
        #polycircle = polycircles.Polycircle(51.507336,-0.127894,1000,100)

        latloncircle = polycircle.to_lon_lat()
        latlonaltcircle = []
        polygon_circle = []
        for element in latloncircle:
            print(element)

        multiplier = 2000
        temperature = int(temp)

        # 'Pal' cap a dalt i cercle al final del pal (a dalt de tot)
        for element in latloncircle:
            print("volta bucle 1")
            tup = (element[0], element[1], (temperature * multiplier) + 10,)
            latlonaltcircle.append(tup)

        # Cilindre (interior / exterior)
        for element in latloncircle:
            print ("volta bucle 2")
            tup = (element[0], element[1], temperature * multiplier,)
            latlonaltcircle.append(tup)
            print ("volta bucle 2")
            tup = (element[0], element[1], 0,)
            latlonaltcircle.append(tup)

        #Un altre cilindre (interior / exterior ?)
        for element in latloncircle:
            print ("volta bucle 3")
            tup = (element[0], element[1], 0,)
            latlonaltcircle.append(tup)
            print ("volta bucle 3")
            tup = (element[0], element[1], temperature * multiplier,)
            latlonaltcircle.append(tup)

        for element in latloncircle:
            print ("volta bucle 4")
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
            tup = (element[0], element[1], (temperature * multiplier) + 20,)
            latlonaltcircle.append(tup)

        pol = shape.newpolygon()
        pol.outerboundaryis = latlonaltcircle

        pol.altitudemode = simplekml.AltitudeMode.relativetoground
        pol.extrude = 5
        self.addColor(pol, flag)

        pol.style.linestyle.width = 5000

        polygon_circle.append(polycircle)

        coord_to_kml = ""
        coord_to_kml1 = ""

        for element in latlonaltcircle:
            #print(element.split("(")[1])
            print(element)
            if coord_to_kml1 == str(""):
                coord_to_kml1 = coord_to_kml1 + str(element[0]) + "," + str(element[1])  + "," + str(element[2])

            else:
                coord_to_kml1 = coord_to_kml1 + " " + str(element[0])  + "," + str(element[1])  + "," + str(element[2])

            print (coord_to_kml1)

        coord_to_kml = coord_to_kml1

        #list_coord_to_kml.append(coord_to_kml)

        return coord_to_kml

    def addColor(self, polygon, flag):
        if flag == 'min':
            polygon.style.polystyle.color = simplekml.Color.blue
            polygon.style.linestyle.color = simplekml.Color.blue
        elif flag =='max':
            polygon.style.polystyle.color = simplekml.Color.red
            polygon.style.linestyle.color = simplekml.Color.red
