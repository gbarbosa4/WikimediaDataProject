import simplekml
import os
import traceback
import collections
from simplekml import Kml

from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from lxml import etree
from WDLG.utils.cylinders import CylindersKml

gxns = '{' + nsmap['gx'] + '}'
stylename = "stylename"
stylename2 = "stylename2"
stylename_icon = "style_only_icon"
stylename_icon_flags1 = "style_only_icon_flag1"
stylename_icon_flags2 = "style_only_icon_flag2"
stylename_icon_flags3 = "style_only_icon_flag3"
stylename_icon_label = "style_icon_label"
stylename_icon_line_poly = "style_icon_line_poly"
style_first = "style_first"
style_second = "style_second"
style_third = "style_third"
style_golden = "style_golden"
style_silver = "style_silver"
style_bronze = "style_bronze"

class GeneratorKML(object):

    data_set = None
    range = 10000000
    tilt = 70
    kml_name = None

    def __init__(self, data_set, kml_name, icon):
        self.data_set = data_set
        self.kml_name = kml_name
        self.icon = icon;

    def KML_file_header(self, icon, tour_name):

        kml_doc = KML.kml(
                     KML.Document(
                       KML.Style(
                         KML.IconStyle(
                           KML.scale('2.5'),
                           KML.Icon(
                             KML.href("../img/"+icon[0])
                           ),
                         ),
                         KML.LabelStyle(
                           KML.color("FF4CBB17"),
                           KML.scale(2)
                         ),
                         KML.BalloonStyle(
                           KML.text("$[description]")
                         ),
                         KML.LineStyle(
                             KML.color('bf00aaff'),
                             KML.width(5)
                         ),
                         id=stylename
                       ),
                       KML.Style(
                         KML.IconStyle(
                           KML.scale('2.5'),
                           KML.Icon(
                             KML.href("../img/"+icon[1])
                           ),
                         ),
                         KML.LabelStyle(
                           KML.color("FF4CBB17"),
                           KML.scale(4)
                         ),
                         KML.LineStyle(
                           KML.color('FFFF0000'),
                           GX.outerColor('FF4CBB17'),
                           GX.physicalWidth('25000'),
                           GX.outerWidth('0.40')
                        ),
                        id=stylename2
                       ),
                       GX.Tour(
                         KML.name(tour_name),
                         GX.Playlist(),
                       ),
                       KML.Folder(
                         KML.name('Features'),
                         KML.Style(
                           KML.ListStyle(
                             KML.listItemType("checkHideChildren")
                           )
                         ),
                         id='features',
                       ),
                     ),
                  )

        return kml_doc

    def KML_file_header_olympic_games(self):
        flags_list = []
        for country in self.data_set.medalTable:
            flags_list.append(country)

        kml_doc = KML.kml(
                    KML.Document(
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('3.5'),
                          KML.Icon(
                            KML.href("../img/"+str(self.data_set.year)+" Summer Olympics.png")
                          ),
                        ),
                        id=stylename_icon
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('3.5'),
                          KML.Icon(
                            KML.href("../img/flags/"+flags_list[0].replace(" ","")+".png")
                          ),
                        ),
                        id=stylename_icon_flags1
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('3.5'),
                          KML.Icon(
                            KML.href("../img/flags/"+flags_list[1].replace(" ","")+".png")
                          ),
                        ),
                        id=stylename_icon_flags2
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('3.5'),
                          KML.Icon(
                            KML.href("../img/flags/"+flags_list[2].replace(" ","")+".png")
                          ),
                        ),
                        id=stylename_icon_flags3
                      ),
                      KML.Style(
                        KML.LabelStyle(
                          KML.color("FFFFFFFF"),
                          KML.scale(1.75)
                        ),
                        KML.IconStyle(
                          KML.scale('3.5'),
                          KML.Icon(
                            KML.hide(True)
                          ),
                        ),
                        id=stylename_icon_label
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("ff793909"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("ff793909"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_first
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("ffee7920"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("ffee7920"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_second
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("fff3b17f"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("fff3b17f"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_third
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("ff00d7ff"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("ff00d7ff"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_golden
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("ffc0c0c0"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("ffc0c0c0"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_silver
                      ),
                      KML.Style(
                        KML.IconStyle(
                          KML.scale('4.0'),
                          KML.Icon(
                            KML.href("")
                          ),
                        ),
                        KML.LineStyle(
                          KML.color("ff53788c"),
                          KML.colorMode("normal"),
                          KML.width(5000),
                        ),
                        KML.PolyStyle(
                          KML.color("ff53788c"),
                          KML.colorMode("normal"),
                          KML.fill(1),
                          KML.outline(1),
                        ),
                        id=style_bronze
                      ),
                      GX.Tour(
                        KML.name("Tour Name"),
                        GX.Playlist(),
                      ),
                      KML.Folder(
                        KML.name('Features'),
                        id='features',
                      ),
                    )
                  )

        return kml_doc

    def find_to_stand_over_the_placemark(self, duration, longitude, latitude, kml_doc):
        # rota fins estar a sobre de la ciutat i apropar-se
        kml_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(duration),
                GX.flyToMode("smooth"),
                KML.LookAt(
                    KML.longitude(longitude),
                    KML.latitude(latitude),
                    KML.altitude(0),
                    KML.heading(0),
                    KML.tilt(0),
                    KML.range(self.range),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        return kml_doc

    def fly_to_the_placemark(self, longitude, latitude, params, kml_doc):
        # fly to the data
        kml_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(params[0]),
                GX.flyToMode("smooth"),
                KML.LookAt(
                    KML.longitude(longitude),
                    KML.latitude(latitude),
                    KML.altitude(params[1]),
                    KML.heading(params[2]),
                    KML.tilt(params[3]),
                    KML.name(params[4].upper()),
                    KML.range(params[5]),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        return kml_doc

    def show_placemark_balloon(self, duration, kml_doc):
        # show the placemark balloon
        kml_doc.Document[gxns + "Tour"].Playlist.append(
            GX.AnimatedUpdate(
                GX.duration(1.0),
                KML.Update(
                    KML.targetHref(),
                    KML.Change(
                        KML.Placemark(
                            KML.visibility(1),
                            GX.balloonVisibility(1),
                        )
                    )
                )
            )
        )

        kml_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(duration)))

        kml_doc.Document[gxns + "Tour"].Playlist.append(
            GX.AnimatedUpdate(
                GX.duration(0.5),
                KML.Update(
                    KML.targetHref(),
                    KML.Change(
                        KML.Placemark(
                            GX.balloonVisibility(0),
                        )
                    )
                )
            )
        )

        return kml_doc

    def rotation_around_placemark(self, data, params, kml_doc):
        # spin around the data
        for aspect in range(0, 360, 10):
            kml_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                GX.duration(params[0]),
                    GX.flyToMode("smooth"),
                    KML.LookAt(
                        KML.longitude(float(data.longitude)),
                        KML.latitude(float(data.latitude)),
                        KML.altitude(params[1]),
                        KML.heading(aspect),
                        KML.tilt(params[2]),
                        KML.range(params[3]),
                        KML.altitudeMode("relativeToGround"),
                    )
                )
            )

        kml_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(1.0)))

        return kml_doc

    def add_placemark_with_balloon(self, data, pm_name, html_name, hash_values, style, kml_doc):
        html_str = ""
        with open(os.getcwd()+"/static/html_balloons/" + html_name, 'r+') as file:
            for line in file:
                html_str = html_str + str(line)
        file.close()
        # add a placemark for the data
        kml_doc.Document.Folder.append(
            KML.Placemark(
                KML.name((pm_name).upper()),
                KML.description(html_str.format(
                    str(hash_values[0]),
                    str(hash_values[1]),
                    str(hash_values[2]),
                    str(hash_values[3]),
                    str(hash_values[4]),
                    str(hash_values[5]),
                    str(hash_values[6]),
                    str(hash_values[7])
                )
                ),
                KML.styleUrl('#{0}'.format(style)),
                #KML.styleUrl('#{0}'.format(stylename)),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(data.longitude),
                        lat=float(data.latitude),
                        alt=50,
                    )
                    )
                ),
                id=pm_name
            )
        )

        return kml_doc

    def add_placemark_line_string(self, data, pm_name, style, kml_doc):
        kml_doc.Document.Folder.append(
          KML.Placemark(
            KML.name(pm_name.upper()),
            KML.MultiGeometry(
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(data[4]),
                        lat=float(data[5]),
                        alt=50,
                    )
                    )
                ),
                KML.LineString(
                  KML.coordinates(
                     '{0},{1},{2} '.format(float(data[2]),float(data[3]),data[6]),
                     '{0},{1},{2} '.format(float(data[0]),float(data[1]),data[6])
                  ),
                )
            ),
            KML.styleUrl('#{0}'.format(style)),
          )
        )

        return kml_doc

    def add_placemark_simple(self, data, pm_name, style, flag, alt, kml_doc):
        if flag == "origin":
            longitude = data.longitude_orig
            latitude = data.latitude_orig
        elif flag == "mouth":
            longitude = data.longitude_mouth
            latitude = data.latitude_mouth
        else:
            longitude = data.longitude
            latitude = data.latitude

        kml_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(pm_name.upper()),
                KML.styleUrl('#{0}'.format(style)),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(longitude),
                        lat=float(latitude),
                        alt=alt,
                    )
                    )
                ),
            )
        )

        return kml_doc

    def add_placemark_simple_line(self, data, iid, kml_doc):

        kml_doc.Document.Folder.append(
            KML.Placemark(
                KML.visibility(0),
                KML.styleUrl('#{0}'.format(stylename)),
                KML.LineString(
                    KML.tessellate(0.1),
                    KML.coordinates("{lon},{lat},{alt} {lon2},{lat2},{alt2}".format(
                        lon=float(data[0]),
                        lat=float(data[1]),
                        alt=0,
                        lon2=float(data[2]),
                        lat2=float(data[3]),
                        alt2=0,
                    )
                    )
                ),
                id = iid
            )
        )

        return kml_doc

    def get_away_from_placemark(self, data, kml_doc):
        # fly to a space viewpoint. Allunyar-se de la ciutat per buscar el seguent punt
        kml_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(8.0),
                GX.flyToMode("bounce"),
                KML.LookAt(
                    KML.longitude(float(data.longitude)),
                    KML.latitude(float(data.latitude)),
                    KML.altitude(0),
                    KML.heading(0),
                    KML.tilt(0),
                    KML.range(self.range),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        return kml_doc

    def placemark_olympic_games_case(self, name, style, coordinates, kml_doc):

        kml_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(name),
                KML.styleUrl('#{0}'.format(style)),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(coordinates),
                ),
            ),
        ),

        return kml_doc

    def placemark_polygon_olympic_games_case(self, style, coordinates, kml_doc):

        kml_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format(style)),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coordinates),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        return kml_doc

    def save_kml_file(self, kml_name, kml_doc):
        # output a KML file (named based on the Python script)
        outfile = open(os.path.join("static/kml/",kml_name+".kml"),"w+")
        outfile.write(etree.tostring(kml_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_Tour_Cities(self):
        tour_kml_doc = self.KML_file_header(["city.png",""],"Tour cities")

        for data in self.data_set:
            longitude = float(data.longitude)
            latitude = float(data.latitude)

            tour_kml_doc = self.find_to_stand_over_the_placemark(6.0,longitude,latitude,tour_kml_doc)
            fly_to_params = [4.0,0,0,0,data.city,7500]
            tour_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,tour_kml_doc)
            tour_kml_doc = self.show_placemark_balloon(12.0,tour_kml_doc)
            rotation_params = [0.75,0,60,2000]
            tour_kml_doc = self.rotation_around_placemark(data,rotation_params,tour_kml_doc)

            hash_values = []
            hash_values.append(str(data.city).upper())
            hash_values.append(str(data.image))
            hash_values.append(str(data.rank))
            hash_values.append(str(data.city))
            hash_values.append(str(data.country))
            hash_values.append(str(data.population))
            hash_values.append(str(data.area))
            hash_values.append(str(data.elevation))

            tour_kml_doc = self.add_placemark_with_balloon(data,data.city,"city_balloon.html",hash_values,stylename,tour_kml_doc)
            tour_kml_doc = self.get_away_from_placemark(data,tour_kml_doc)

        return self.save_kml_file(self.kml_name, tour_kml_doc)


    def generateKML_premierLeague_Stadiums(self):
        stadiums_kml_doc = self.KML_file_header(["stadium.png",""],"Stadium Tour")
        longitude = float(self.data_set.longitude)
        latitude = float(self.data_set.latitude)
        fly_to_params = [6.0,0,0,70,self.data_set.stadiumName,400]
        stadiums_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,stadiums_kml_doc)
        stadiums_kml_doc = self.show_placemark_balloon(8.0,stadiums_kml_doc)
        rotation_params = [0.80,0,70,600]
        stadiums_kml_doc = self.rotation_around_placemark(self.data_set,rotation_params,stadiums_kml_doc)

        hash_values = []
        hash_values.append(str(self.data_set.stadiumName).upper())
        hash_values.append(str(self.data_set.stadiumImage))
        hash_values.append(str(self.data_set.clubName))
        hash_values.append(str(self.data_set.clubShieldImage))
        hash_values.append(str(self.data_set.clubFounded))
        hash_values.append(str(self.data_set.clubCoach))
        hash_values.append(str(self.data_set.clubCity))
        hash_values.append(str(self.data_set.stadiumCapacity))

        stadiums_kml_doc = self.add_placemark_with_balloon(self.data_set,self.data_set.stadiumName,"stadium_balloon.html",hash_values,stylename,stadiums_kml_doc)

        return self.save_kml_file(self.kml_name, stadiums_kml_doc)

    def generateKML_Longest_Rivers(self):
        rivers_kml_doc = self.KML_file_header(["point.png","river.png"],"Longest Rivers Tour")

        for data in self.data_set:
            data_list = []
            # print(data.river," ",data.longitude_orig," ",data.latitude_orig," ",data.longitude_mouth," ",data.latitude_mouth)
            long_med = (float(data.longitude_mouth)+float(data.longitude_orig))/2.0
            lat_med = (float(data.latitude_mouth)+float(data.latitude_orig))/2.0

            data_list.append(float(data.longitude_orig))
            data_list.append(float(data.latitude_orig))
            data_list.append(float(data.longitude_mouth))
            data_list.append(float(data.latitude_mouth))
            data_list.append(float(long_med))
            data_list.append(float(lat_med))
            data_list.append(1350.0)

            rivers_kml_doc = self.add_placemark_line_string(data_list,data.river,stylename2,rivers_kml_doc)
            rivers_kml_doc = self.add_placemark_simple(data,data.origin,stylename,"origin",50,rivers_kml_doc)
            rivers_kml_doc = self.add_placemark_simple(data,data.mouth,stylename,"mouth",50,rivers_kml_doc)

        return self.save_kml_file(self.kml_name, rivers_kml_doc)

    def generateKML_Tour_Experience(self,data_points):
        tour_experience_kml_doc = self.KML_file_header(["",""],"Tour Experience")
        longitude = str(data_points[0]).split(",")[0].split("['")[1]
        latitude = str(data_points[0]).split(",")[1].split("']")[0]
        tour_experience_kml_doc = self.find_to_stand_over_the_placemark(4.0,longitude,latitude,tour_experience_kml_doc)
        fly_to_params = [4,0,-100,65,"river tour experience",80000]
        tour_experience_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,tour_experience_kml_doc)

        i=1
        while i < len(data_points):
            longitude = str(data_points[i]).split(",")[0].split("['")[1]
            latitude = str(data_points[i]).split(",")[1].split("']")[0]
            fly_to_params = [1.75,0,-100,45,"river tour experience",10000]
            tour_experience_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,tour_experience_kml_doc)

            i=i+1

        return self.save_kml_file(self.kml_name, tour_experience_kml_doc)

    def generateKML_Line_Track_Experience (self,data_points):
        linetrack_experience_kml_doc = self.KML_file_header(["",""],"Line Track Experience")

        longitude = str(data_points[0]).split(",")[0].split("['")[1]
        latitude = str(data_points[0]).split(",")[1].split("']")[0]
        linetrack_experience_kml_doc = self.find_to_stand_over_the_placemark(2.0,longitude,latitude,linetrack_experience_kml_doc)

        i = 0
        while i < len(data_points)-1:
            data_list = []
            data_list.append(str(data_points[i]).split(",")[0].split("['")[1])
            data_list.append(str(data_points[i]).split(",")[1].split("']")[0])
            data_list.append(str(data_points[i+1]).split(",")[0].split("['")[1])
            data_list.append(str(data_points[i+1]).split(",")[1].split("']")[0])
            iid = str((i+1))
            linetrack_experience_kml_doc = self.add_placemark_simple_line(data_list,iid,linetrack_experience_kml_doc)

            i = i+1

        i = 0
        while i < len(data_points)-1:
            linetrack_experience_kml_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(0.06)))

            linetrack_experience_kml_doc.Document[gxns + "Tour"].Playlist.append(
                GX.AnimatedUpdate(
                    KML.Update(
                        KML.Change(
                            KML.Placemark(
                                KML.visibility(1),
                                targetId=str((i+1)),
                            )
                        )
                    )
                )
            )

            i = i+1

        return self.save_kml_file(self.kml_name, linetrack_experience_kml_doc)

    def generateKML_Spanish_Airports(self):
        airoprts_kml_doc = self.KML_file_header(["airport.png",""],"Spanish Airports Tour")

        for data in self.data_set:
            longitude = float(data.longitude)
            latitude = float(data.latitude)

            airoprts_kml_doc = self.find_to_stand_over_the_placemark(6.0,longitude,latitude,airoprts_kml_doc)
            fly_to_params = [10.0,0,0,0,data.city,7500]
            airoprts_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,airoprts_kml_doc)
            airoprts_kml_doc = self.show_placemark_balloon(12.0,airoprts_kml_doc)
            rotation_params = [1.25,0,60,2000]
            airoprts_kml_doc = self.rotation_around_placemark(data,rotation_params,airoprts_kml_doc)

            hash_values = []
            hash_values.append(str(data.city).upper())
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))
            hash_values.append(str(data.city))

            airoprts_kml_doc = self.add_placemark_with_balloon(data,data.city,"airport_balloon.html",hash_values,stylename,airoprts_kml_doc)
            airoprts_kml_doc = self.get_away_from_placemark(data,airoprts_kml_doc)

        return self.save_kml_file(self.kml_name, airoprts_kml_doc)

    def getValues_countryName(self,dict_medal_table,option,position):
        value = []
        if option == "total":
            for key in dict_medal_table:
                value.append(key)
                value.append(dict_medal_table[key].split("|")[4])

        elif option == "medals":
            key_list = []
            for key in dict_medal_table:
                key_list.append(key)

            key = key_list[position-1]
            value.append(key)
            i = 1
            while i<4:
                value.append(dict_medal_table[key].split("|")[i])
                i = i + 1

        return value

    def preparing_KML_data(self, data, values_option, extra, index):
        coordinates = {}
        data_dict = {}

        coordinates["lat"] = data[0]
        coordinates["lng"] = data[1]

        values = self.getValues_countryName(data[2],values_option,index)

        data_dict["name"] = data[3]
        data_dict["description"] = values
        data_dict["coordinates"] = coordinates
        data_dict["extra"] = extra

        return data_dict

    def medals_data_cylinders(self, data, num_medals, medal, kml_doc):
        pointer_medal = data[0][medal]
        coord_to_kml_medal = data[1][medal]
        if medal == "golden":
            kml_doc = self.placemark_polygon_olympic_games_case(style_golden,coord_to_kml_medal,kml_doc)
        if medal == "silver":
            kml_doc = self.placemark_polygon_olympic_games_case(style_silver,coord_to_kml_medal,kml_doc)
        if medal == "bronze":
            kml_doc = self.placemark_polygon_olympic_games_case(style_bronze,coord_to_kml_medal,kml_doc)

        alt_medal = str(pointer_medal).split(",")[2]
        num_alt_medal = float(alt_medal)/3.0
        pointer_medal_label = str(pointer_medal).replace(str(alt_medal),str(num_alt_medal))
        kml_doc = self.placemark_olympic_games_case(num_medals,stylename_icon_label,pointer_medal_label,kml_doc)

        return kml_doc

    def podium_data_cylinders(self, data, name, medal_table, position, kml_doc):
        i = 0
        pointer = data[0][position]
        if position == "first":
            kml_doc = self.placemark_olympic_games_case("",stylename_icon_flags1,pointer,kml_doc)
            i=1
        if position == "second":
            kml_doc = self.placemark_olympic_games_case("",stylename_icon_flags2,pointer,kml_doc)
            i=2
        if position == "third":
            kml_doc = self.placemark_olympic_games_case("",stylename_icon_flags3,pointer,kml_doc)
            i=3

        alt = str(pointer).split(",")[2]
        pointer_label = str(pointer).replace(str(alt),str(float(alt)-3000.0))
        kml_doc = self.placemark_olympic_games_case(name[0],stylename_icon_label,pointer_label,kml_doc)
        pointer_medals = str(pointer).replace(str(alt),str(float(alt)-5000.0))
        kml_doc = self.placemark_olympic_games_case("Total: "+name[1]+" medals.",stylename_icon_label,pointer_medals,kml_doc)
        coord_to_kml = data[1][position]
        if position == "first":
            kml_doc = self.placemark_polygon_olympic_games_case(style_first,coord_to_kml,kml_doc)
        if position == "second":
            kml_doc = self.placemark_polygon_olympic_games_case(style_second,coord_to_kml,kml_doc)
        if position == "third":
            kml_doc = self.placemark_polygon_olympic_games_case(style_third,coord_to_kml,kml_doc)

        #------ Little cylinders.. every country number of separated medals. Bucle 3 voltes -------
        data_list = []
        data_list.append(float(str(pointer).split(",")[1]))
        data_list.append(float(str(pointer).split(",")[0]))
        data_list.append(medal_table)
        data_list.append("cylinder_medals")

        data_dict_medals = self.preparing_KML_data(data_list,"medals","medals",i)

        cilinder_medals = CylindersKml("",data_dict_medals)
        coord_to_kml_dict_medals = cilinder_medals.makeKML()

        print("-- ",position," ",data_dict_medals["description"][0])
        print(data_dict_medals["description"][1])
        print(data_dict_medals["description"][2])
        print(data_dict_medals["description"][3])

        kml_doc = self.medals_data_cylinders(coord_to_kml_dict_medals,data_dict_medals["description"][1],"golden",kml_doc)
        kml_doc = self.medals_data_cylinders(coord_to_kml_dict_medals,data_dict_medals["description"][2],"silver",kml_doc)
        kml_doc = self.medals_data_cylinders(coord_to_kml_dict_medals,data_dict_medals["description"][3],"bronze",kml_doc)

        return kml_doc

    def generateKML_Olympic_Games(self):
        olympic_games_kml_doc = self.KML_file_header_olympic_games()
        longitude = float(self.data_set.longitude)
        latitude = float(self.data_set.latitude)

        fly_to_params = [6.0,0,-55,65,self.data_set.hostCity,70000]
        olympic_games_kml_doc = self.fly_to_the_placemark(longitude,latitude,fly_to_params,olympic_games_kml_doc)
        olympic_games_kml_doc = self.add_placemark_simple(self.data_set,self.data_set.hostCity+" "+str(self.data_set.year),stylename_icon_label,"",25000,olympic_games_kml_doc)
        olympic_games_kml_doc = self.add_placemark_simple(self.data_set,"",stylename_icon,"",26500,olympic_games_kml_doc)

        data_list = []
        data_list.append(float(self.data_set.latitude)-float(0.02))
        data_list.append(float(self.data_set.longitude)-float(0.05))
        data_list.append(self.data_set.medalTable)
        data_list.append(self.data_set.hostCity + " " + str(self.data_set.year))

        data_dict = self.preparing_KML_data(data_list,"total","podium",0)
        print(data_dict)
        cilinders = CylindersKml("",data_dict)
        coord_to_kml_dict = cilinders.makeKML()

        olympic_games_kml_doc = self.podium_data_cylinders(coord_to_kml_dict,[data_dict["description"][0],data_dict["description"][1]],self.data_set.medalTable,"first",olympic_games_kml_doc)
        olympic_games_kml_doc = self.podium_data_cylinders(coord_to_kml_dict,[data_dict["description"][2],data_dict["description"][3]],self.data_set.medalTable,"second",olympic_games_kml_doc)
        olympic_games_kml_doc =self.podium_data_cylinders(coord_to_kml_dict,[data_dict["description"][4],data_dict["description"][5]],self.data_set.medalTable,"third",olympic_games_kml_doc)

        return self.save_kml_file(self.kml_name, olympic_games_kml_doc)
