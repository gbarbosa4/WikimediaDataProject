import simplekml
import os
import traceback
from simplekml import Kml

from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pykml.parser import Schema
from lxml import etree
from WDLG.utils.cylinders import CylindersKml


class GeneratorKML(object):

    data_set = None
    range = 10000000
    tilt = 70
    kml_name = None

    def __init__(self, data_set, kml_name, icon):
        self.data_set = data_set
        self.kml_name = kml_name
        self.icon = icon;

    def generateKML_Tour_Cities(self):

        # define a variable for the Google Extensions namespace URL string
        gxns = '{' + nsmap['gx'] + '}'
        stylename = "sn_shaded_dot"
        stylename2 = "sn_shaded_dot2"
        # start with a base KML tour and playlist
        tour_doc = KML.kml(
                        KML.Document(
                                KML.Style(
                                    KML.IconStyle(
                                        KML.scale('2.5'),
                                        KML.Icon(
                                            KML.href('img/city_icon.png')
                                        ),
                                    ),
                                    KML.LabelStyle(
                                        KML.color("FF4CBB17"),
                                        KML.scale(2)
                                    ),
                                    KML.BalloonStyle(
                                        KML.text("$[description]")
                                    ),
                                    id=stylename
                                ),
                                GX.Tour(
                                    KML.name("Tour cities"),
                                    GX.Playlist(),
                                ),
                                KML.Folder(
                                    KML.name('Features'),
                                    id='features',
                                ),
                        ),
                    )

        for data in self.data_set:
            # import ipdb; ipdb.set_trace()
            # fly to a space viewpoint
            # rota fins estar a sobre de la ciutat i apropar-se
            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(6),
                    GX.flyToMode("smooth"),
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

            # fly to the data
            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(10),
                    GX.flyToMode("bounce"),
                    KML.LookAt(
                        KML.longitude(float(data.longitude)),
                        KML.latitude(float(data.latitude)),
                        KML.altitude(0),
                        KML.heading(0),
                        KML.tilt(0),
                        KML.name((data.city).upper()),
                        KML.range(7500),
                        KML.altitudeMode("relativeToGround"),
                    )
                ),
            )

            # show the placemark balloon
            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.AnimatedUpdate(
                    GX.duration(1.0),
                    KML.Update(
                        KML.targetHref(),
                        KML.Change(
                            KML.Placemark(
                                KML.visibility(1),
                                GX.balloonVisibility(1),
                                targetId=data.city.replace(' ', '_')
                            )
                        )
                    )
                )
            )

            tour_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(12.0)))

            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.AnimatedUpdate(
                    GX.duration(0.5),
                    KML.Update(
                        KML.targetHref(),
                        KML.Change(
                            KML.Placemark(
                                GX.balloonVisibility(0),
                                targetId=data.city.replace(' ', '_')
                            )
                        )
                    )
                )
            )

            # spin around the data
            for aspect in range(0, 360, 10):
                tour_doc.Document[gxns + "Tour"].Playlist.append(
                    GX.FlyTo(
                        GX.duration(0.75),
                        GX.flyToMode("smooth"),
                        KML.LookAt(
                            KML.longitude(float(data.longitude)),
                            KML.latitude(float(data.latitude)),
                            KML.altitude(0),
                            KML.heading(aspect),
                            KML.tilt(60),
                            KML.range(2000),
                            KML.altitudeMode("relativeToGround"),
                        )
                    )
                )
            tour_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(1.0)))

            # tour_doc.Document[gxns+"Tour"].Playlist.append(
            #        GX.TourControl(GX.playMode("pause"))
            #    )

            # add a placemark for the data
            tour_doc.Document.Folder.append(
                KML.Placemark(
                    KML.name((data.city).upper()),
                    KML.description(
                    "<table width='400' border='1' cellspacing='0' cellpadding='4' bgcolor='#E6E6E6'> \
                      <tr> \
                        <td colspan='2' align='center'> \
                          <h3><font color='#000000'>{city_name_upper}</font></h3> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2' align='center'> \
                          <img src='{image}' alt='picture' width='400' height='280' /> \
                        </td> \
                      </tr> \
                      <tr></tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Ranking:</b></font> \
                          <font size='4'>{ranking}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>City name:</b></font> \
                          <font size='4'>{city_name}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Country:</b></font> \
                          <font size='4'>{country}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Population:</b></font> \
                          <font size='4'>{population}</font> <font size='4'>million people</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Area:</b></font> \
                          <font size='4'>{area}</font> <font size='4'>square kilometers</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Elevation:</b></font> \
                          <font size='4'>{elevation}</font> <font size='4'>metres</font> \
                        </td> \
                      </tr> \
                    </table>".format(
                            city_name_upper=data.city.upper(),
                            ranking=data.rank,
                            city_name=data.city,
                            image=data.image,
                            population=round(float(data.population)/float(1000000),3),
                            country=data.country,
                            area=data.area,
                            elevation=data.elevation,
                    )
                    ),
                    KML.styleUrl('#{0}'.format(stylename)),
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
                    id=data.city.replace(' ', '_')
                )
            )


            # fly to a space viewpoint. Allunyar-se de la ciutat per buscar el seguent punt
            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(12),
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

        # check that the KML document is valid using the Google Extension XML Schema
        # assert(Schema("kml22gx.xsd").validate(tour_doc))

        # print (etree.tostring(tour_doc, pretty_print=True))

        # output a KML file (named based on the Python script)
        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(tour_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_premierLeague_Stadiums(self):

        # define a variable for the Google Extensions namespace URL string
        gxns = '{' + nsmap['gx'] + '}'
        stylename = "sn_shaded_dot"
        stylename2 = "sn_shaded_dot2"
        # start with a base KML tour and playlist
        airports_doc = KML.kml(
                        KML.Document(
                                KML.Style(
                                    KML.IconStyle(
                                        KML.scale('2.5'),
                                        KML.Icon(
                                            KML.href('http://maps.google.com/mapfiles/kml/pal2/icon49.png')
                                        ),
                                    ),
                                    KML.LabelStyle(
                                        KML.color("FF4CBB17"),
                                        KML.scale(1.2)
                                    ),
                                    KML.BalloonStyle(
                                        KML.text("$[description]")
                                    ),
                                    id=stylename
                                ),
                                KML.Folder(
                                    KML.name('Features'),
                                    id='features',
                                ),
                                GX.Tour(
                                    KML.name('Stadium Tour'),
                                    GX.Playlist(),
                                ),
                        ),
                    )

        # fly to the data
        airports_doc.Document.Folder.append(
            GX.FlyTo(
                GX.duration(10),
                GX.flyToMode("bounce"),
                KML.LookAt(
                    KML.longitude(float(self.data_set.longitude)),
                    KML.latitude(float(self.data_set.latitude)),
                    KML.altitude(0),
                    KML.heading(0),
                    KML.tilt(70),
                    KML.name((self.data_set.stadiumName).upper()),
                    KML.range(400),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )
        #GX.Wait(GX.duration(10.0))

        # show the placemark balloon
        airports_doc.Document[gxns + "Tour"].Playlist.append(
            GX.AnimatedUpdate(
                GX.duration(1.0),
                KML.Update(
                    KML.targetHref(),
                    KML.Change(
                        KML.Placemark(
                            KML.visibility(1),
                            GX.balloonVisibility(1),
                            targetId=self.data_set.stadiumName.replace(' ', '_')
                        )
                    )
                )
            )
        )

        airports_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(8.0)))

        airports_doc.Document[gxns + "Tour"].Playlist.append(
            GX.AnimatedUpdate(
                GX.duration(0.5),
                KML.Update(
                    KML.targetHref(),
                    KML.Change(
                        KML.Placemark(
                            GX.balloonVisibility(0),
                            targetId=self.data_set.stadiumName.replace(' ', '_')
                        )
                    )
                )
            )
        )

        # spin around the data
        for aspect in range(0, 360, 10):
            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(0.80),
                    GX.flyToMode("smooth"),
                    KML.LookAt(
                        KML.longitude(self.data_set.longitude),
                        KML.latitude(self.data_set.latitude),
                        KML.altitude(0),
                        KML.heading(aspect),
                        KML.tilt(70),
                        KML.range(600),
                        KML.altitudeMode("relativeToGround"),
                    )
                )
            )

        # add a placemark/BalloonStyle for the data
        airports_doc.Document.Folder.append(
            KML.Placemark(
                KML.name((self.data_set.stadiumName).upper()),
                KML.description(
                "<table width='400' border='1' cellspacing='1' cellpadding='4' bgcolor='#E6E6E6'> \
                  <tr> \
                    <td colspan='3' align='center'> \
                      <h3><font size='6' color='#000000'>{stadium_name}</font></h3> \
                    </td> \
                  </tr> \
                  <tr> \
                    <td bgcolor='#A4A4A4' colspan='3' align='center'> \
                      <img src='{stadium_image}' alt='picture' width='340' height='200' /> \
                    </td> \
                  </tr> \
                  <tr></tr> \
                  <tr> \
                    <td colspan='2'> \
                      <font size='4'><b>Football club name: </b></font> \
                      <font size='5'>{club_name}</font> \
                    </td> \
                    <td colspan='2' align='center'> \
                      <img src='{club_shield_image}' alt='picture' width='50' height='50' /> \
                    </td> \
                  </tr> \
                  <tr> \
                    <td colspan='3'> \
                      <font size='4'><b>Club founded in </b></font> \
                      <font size='5'>{club_founded}</font> \
                    </td> \
                  </tr> \
                  <tr> \
                    <td colspan='3'> \
                      <font size='4'><b>Manager: </b></font> \
                      <font size='5'>{club_coach}</font> \
                    </td> \
                  </tr> \
                  <tr> \
                    <td colspan='3'> \
                      <font size='4'><b>City: </b></font> \
                      <font size='5'>{club_city}</font> \
                    </td> \
                  </tr> \
                  <tr> \
                    <td colspan='3'> \
                      <font size='4'><b>Stadium capacity: </b></font> \
                      <font size='5'>{stadium_capacity}</font> <font size='4'> people</font> \
                    </td> \
                  </tr> \
                </table>".format(
                        stadium_name = self.data_set.stadiumName.upper(),
                        club_shield_image = self.data_set.clubShieldImage,
                        stadium_image = self.data_set.stadiumImage,
                        club_name = self.data_set.clubName,
                        club_founded = self.data_set.clubFounded,
                        club_coach = self.data_set.clubCoach,
                        club_city = self.data_set.clubCity,
                        stadium_capacity = self.data_set.stadiumCapacity,
                )
                ),
                KML.styleUrl('#{0}'.format(stylename)),
                #KML.styleUrl('#{0}'.format(stylename)),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(self.data_set.longitude),
                        lat=float(self.data_set.latitude),
                        alt=50,
                    )
                    )
                ),
                id=self.data_set.stadiumName.replace(' ', '_')
            )
        )

        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(airports_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_Longest_Rivers(self):

        stylename = "sn_shaded_dot"
        stylename_orig = "sn_shaded_dot_orig"
        stylename_mouth = "sn_shaded_dot_mouth"

        doc = KML.kml(
            KML.Document(
                GX.Tour(
                    KML.name("Play me!"),
                    GX.Playlist(),
                ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('2.5'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/shapes/water.png')
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
                    id=stylename
                ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('2.5'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/paddle/O.png')
                        ),
                    ),
                    KML.LabelStyle(
                        KML.color("FFFF0000"),
                        KML.scale(0.75)
                    ),
                    id=stylename_orig
                ),
                KML.Style(
                    KML.IconStyle(
                        KML.scale('2.5'),
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/kml/paddle/M.png')
                        ),
                    ),
                    KML.LabelStyle(
                        KML.color("FFFFOOOO"),
                        KML.scale(0.75)
                    ),
                    id=stylename_mouth
                ),
                KML.Folder(
                    KML.name('Features'),
                    id='features',
                )
            )
        )

        for data in self.data_set:

            long_med = (float(data.longitude_mouth)+float(data.longitude_orig))/2.0
            lat_med = (float(data.latitude_mouth)+float(data.latitude_orig))/2.0

            doc.Document.Folder.append(
              KML.Placemark(
                KML.name((data.river).upper()),
                KML.styleUrl('#{0}'.format(stylename)),
                KML.MultiGeometry(
                    KML.Point(
                        KML.extrude(0),
                        KML.altitudeMode("relativeToGround"),
                        KML.coordinates("{lon},{lat},{alt}".format(
                            lon=float(long_med),
                            lat=float(lat_med),
                            alt=50,
                        )
                        )
                    ),
                    KML.LineString(
                      KML.coordinates(
                         '{0},{1},{2} '.format(float(data.longitude_mouth),float(data.latitude_mouth),1350.0),
                         '{0},{1},{2} '.format(float(data.longitude_orig),float(data.latitude_orig),1350.0)
                        #(float(data.longitude),float(data.latitude),0.0 float(data.longitude)+0.21000,float(data.latitude)-30.4032,0.0)
                      )
                    ),
                )
              )
            )

            doc.Document.Folder.append(
                KML.Placemark(
                    KML.name((data.origin).upper()),
                    KML.styleUrl('#{0}'.format(stylename_orig)),
                    KML.Point(
                        KML.extrude(0),
                        KML.altitudeMode("relativeToGround"),
                        KML.coordinates("{lon},{lat},{alt}".format(
                            lon=float(data.longitude_orig),
                            lat=float(data.latitude_orig),
                            alt=50,
                        )
                        )
                    ),
                )
            )

            doc.Document.Folder.append(
                KML.Placemark(
                    KML.name((data.mouth).upper()),
                    KML.styleUrl('#{0}'.format(stylename_mouth)),
                    KML.Point(
                        KML.extrude(0),
                        KML.altitudeMode("relativeToGround"),
                        KML.coordinates("{lon},{lat},{alt}".format(
                            lon=float(data.longitude_mouth),
                            lat=float(data.latitude_mouth),
                            alt=50,
                        )
                        )
                    ),
                )
            )

        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_Nile_Tour_Experience(self,data_points):

        print (data_points[0].split(",")[0])
        gxns = '{' + nsmap['gx'] + '}'
        stylename = "sn_shaded_dot"
        stylename2 = "sn_shaded_dot2"
        # start with a base KML tour and playlist
        tour_doc = KML.kml(
                        KML.Document(
                                KML.Style(
                                    KML.IconStyle(
                                        KML.scale('2.5'),
                                        KML.Icon(
                                            KML.href('http://earth.google.com/images/kml-icons/track-directional/track-8.png')
                                        ),
                                    ),
                                    KML.LabelStyle(
                                        KML.color("FF4CBB17"),
                                        KML.scale(2)
                                    ),
                                    KML.BalloonStyle(
                                        KML.text("$[description]")
                                    ),
                                    id=stylename
                                ),
                                GX.Tour(
                                    KML.name("Nile Experience"),
                                    GX.Playlist(),
                                ),
                                KML.Folder(
                                    KML.name('Features'),
                                    id='features',
                                ),
                        ),
                    )

        # rota fins estar a sobre de la ciutat i apropar-se
        tour_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(4),
                GX.flyToMode("smooth"),
                KML.LookAt(
                    KML.longitude(31.2560),
                    KML.latitude(15.30302),
                    KML.altitude(0),
                    KML.heading(0),
                    KML.tilt(0),
                    KML.range(self.range),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        # fly to the data
        tour_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(4),
                GX.flyToMode("bounce"),
                KML.LookAt(
                    KML.longitude(data_points[0].split(",")[0]),
                    KML.latitude(data_points[0].split(",")[1]),
                    KML.altitude(0),
                    KML.heading(-100),
                    KML.tilt(65),
                    KML.name("ffffffff".upper()),
                    KML.range(80000),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        i=1
        while i < len(data_points):

            # fly to the data
            tour_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(1.75),
                    GX.flyToMode("smooth"),
                    KML.LookAt(
                        KML.longitude(data_points[i].split(",")[0]),
                        KML.latitude(data_points[i].split(",")[1]),
                        KML.altitude(0),
                        KML.heading(-100),
                        KML.tilt(45),
                        KML.name("ffffffff".upper()),
                        KML.range(10000),
                        KML.altitudeMode("relativeToGround"),
                    )
                ),
            )
            i=i+1

        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(tour_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_Nile_Line_Experience (self,data_points):
        print(len(data_points))
        gxns = '{' + nsmap['gx'] + '}'
        line_style = "line-style"
        stylename2 = "sn_shaded_dot2"
        # start with a base KML tour and playlist
        river_doc = KML.kml(
                        KML.Document(
                                KML.name("Name document"),
                                KML.open(1),
                                KML.Style(
                                    KML.LineStyle(
                                        KML.color('bf00aaff'),
                                        KML.width(5)
                                    ),
                                    id = line_style
                                ),
                                GX.Tour(
                                    KML.name("Nile Experience"),
                                    GX.Playlist(),
                                ),
                                KML.Folder(
                                    KML.name('Features'),
                                    KML.Style(
                                        KML.ListStyle(
                                            KML.listItemType("checkHideChildren")
                                        )
                                    )
                                ),
                        ),
                    )

        # rota fins estar a sobre de la ciutat i apropar-se
        river_doc.Document[gxns + "Tour"].Playlist.append(
            GX.FlyTo(
                GX.duration(2),
                GX.flyToMode("smooth"),
                KML.LookAt(
                    KML.longitude(31.2560),
                    KML.latitude(15.30302),
                    KML.altitude(0),
                    KML.heading(0),
                    KML.tilt(0),
                    KML.range(self.range),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        )

        i = 0

        while i < len(data_points)-1:

            river_doc.Document.Folder.append(
                KML.Placemark(
                    KML.name(str((i+1))),
                    KML.visibility(0),
                    KML.styleUrl('#{0}'.format(line_style)),
                    KML.LineString(
                        KML.tessellate(0.1),
                        KML.coordinates("{lon},{lat},{alt} {lon2},{lat2},{alt2}".format(
                            lon=float(data_points[i].split(",")[0]),
                            lat=float(data_points[i].split(",")[1]),
                            alt=0,
                            lon2=float(data_points[i+1].split(",")[0]),
                            lat2=float(data_points[i+1].split(",")[1]),
                            alt2=0,
                        )
                        )
                    ),
                    id = str((i+1))
                )
            )

            i = i+1

        i = 0
        while i < len(data_points)-1:

            river_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(0.01)))

            river_doc.Document[gxns + "Tour"].Playlist.append(
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

        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(river_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def generateKML_Spanish_Airports(self):

        # define a variable for the Google Extensions namespace URL string
        gxns = '{' + nsmap['gx'] + '}'
        stylename = "sn_shaded_dot"
        stylename2 = "sn_shaded_dot2"
        # start with a base KML tour and playlist
        airports_doc = KML.kml(
                        KML.Document(
                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('2.5'),
                                    KML.Icon(
                                        KML.href('http://maps.google.com/mapfiles/kml/shapes/airports.png')
                                    ),
                                ),
                                KML.LabelStyle(
                                    KML.color("FF4CBB17"),
                                    KML.scale(2)
                                ),
                                KML.BalloonStyle(
                                    KML.text("$[description]")
                                ),
                                id=stylename
                            ),
                            GX.Tour(
                                KML.name("Spanish Airports"),
                                GX.Playlist(),
                            ),
                            KML.Folder(
                                KML.name('Features'),
                                id='features',
                            ),
                    ),
                )

        for data in self.data_set:
            # import ipdb; ipdb.set_trace()
            # fly to a space viewpoint
            # rota fins estar a sobre de la ciutat i apropar-se
            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(6),
                    GX.flyToMode("smooth"),
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

            # fly to the data
            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(10),
                    GX.flyToMode("bounce"),
                    KML.LookAt(
                        KML.longitude(float(data.longitude)),
                        KML.latitude(float(data.latitude)),
                        KML.altitude(0),
                        KML.heading(0),
                        KML.tilt(0),
                        KML.name((data.city).upper()),
                        KML.range(7500),
                        KML.altitudeMode("relativeToGround"),
                    )
                ),
            )

            # show the placemark balloon
            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.AnimatedUpdate(
                    GX.duration(1.0),
                    KML.Update(
                        KML.targetHref(),
                        KML.Change(
                            KML.Placemark(
                                KML.visibility(1),
                                GX.balloonVisibility(1),
                                targetId=data.city.replace(' ', '_')
                            )
                        )
                    )
                )
            )

            airports_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(12.0)))

            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.AnimatedUpdate(
                    GX.duration(0.5),
                    KML.Update(
                        KML.targetHref(),
                        KML.Change(
                            KML.Placemark(
                                GX.balloonVisibility(0),
                                targetId=data.city.replace(' ', '_')
                            )
                        )
                    )
                )
            )

            # spin around the data
            for aspect in range(0, 360, 10):
                airports_doc.Document[gxns + "Tour"].Playlist.append(
                    GX.FlyTo(
                        GX.duration(1.25),
                        GX.flyToMode("smooth"),
                        KML.LookAt(
                            KML.longitude(float(data.longitude)),
                            KML.latitude(float(data.latitude)),
                            KML.altitude(0),
                            KML.heading(aspect),
                            KML.tilt(60),
                            KML.range(2000),
                            KML.altitudeMode("relativeToGround"),
                        )
                    )
                )
            airports_doc.Document[gxns + "Tour"].Playlist.append(GX.Wait(GX.duration(1.0)))

            # tour_doc.Document[gxns+"Tour"].Playlist.append(
            #        GX.TourControl(GX.playMode("pause"))
            #    )

            # add a placemark for the data
            airports_doc.Document.Folder.append(
                KML.Placemark(
                    KML.name((data.city).upper()),
                    KML.description(
                    "<table width='400' border='1' cellspacing='0' cellpadding='4' bgcolor='#E6E6E6'> \
                      <tr> \
                        <td colspan='2' align='center'> \
                          <h3><font color='#000000'>{city_name_upper}</font></h3> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2' align='center'> \
                          <img src='{image}' alt='picture' width='400' height='280' /> \
                        </td> \
                      </tr> \
                      <tr></tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Ranking:</b></font> \
                          <font size='4'>{ranking}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>City name:</b></font> \
                          <font size='4'>{city_name}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Country:</b></font> \
                          <font size='4'>{country}</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Population:</b></font> \
                          <font size='4'>{population}</font> <font size='4'>million people</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Area:</b></font> \
                          <font size='4'>{area}</font> <font size='4'>square kilometers</font> \
                        </td> \
                      </tr> \
                      <tr> \
                        <td colspan='2'> \
                          <font size='4'><b>Elevation:</b></font> \
                          <font size='4'>{elevation}</font> <font size='4'>metres</font> \
                        </td> \
                      </tr> \
                    </table>".format(
                            city_name_upper=data.city.upper(),
                            ranking=data.city,
                            city_name=data.city,
                            image=data.image,
                            population=data.opening,
                            country=data.airport,
                            area=data.airport,
                            elevation=data.airport,
                    )
                    ),
                    KML.styleUrl('#{0}'.format(stylename)),
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
                    id=data.city.replace(' ', '_')
                )
            )


            # fly to a space viewpoint. Allunyar-se de la ciutat per buscar el seguent punt
            airports_doc.Document[gxns + "Tour"].Playlist.append(
                GX.FlyTo(
                    GX.duration(12),
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

        # check that the KML document is valid using the Google Extension XML Schema
        # assert(Schema("kml22gx.xsd").validate(tour_doc))

        # print (etree.tostring(tour_doc, pretty_print=True))

        # output a KML file (named based on the Python script)
        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(airports_doc, encoding="unicode"))
        outfile.close()

        return outfile

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

    def generateKML_Olympic_Games(self):
        gxns = '{' + nsmap['gx'] + '}'
        stylename = "sn_shaded_dot"
        stylename2 = "sn_shaded_dot2"

        coordinates = {}
        coordinates["lat"] = float(self.data_set.latitude)-float(0.02)
        coordinates["lng"] = float(self.data_set.longitude)-float(0.05)

        values = self.getValues_countryName(self.data_set.medalTable,"total",0)

        data_dict = {}
        data_dict["name"] = self.data_set.hostCity + " " + str(self.data_set.year)
        data_dict["description"] = values
        data_dict["coordinates"] = coordinates
        data_dict["extra"] = "podium"

        cilinders = CylindersKml("",data_dict)

        coord_to_kml_dict = cilinders.makeKML()

        pointer_first = coord_to_kml_dict[0]["first"]
        pointer_second = coord_to_kml_dict[0]["second"]
        pointer_third = coord_to_kml_dict[0]["third"]

        alt_first = str(pointer_first).split(",")[2]
        alt_second = str(pointer_second).split(",")[2]
        alt_third = str(pointer_third).split(",")[2]

        num_alt1 = float(alt_first)-3000.0
        num_alt1m = float(alt_first)-5000.0
        num_alt2 = float(alt_second)-3000.0
        num_alt2m = float(alt_second)-5000.0
        num_alt3 = float(alt_third)-3000.0
        num_alt3m = float(alt_third)-5000.0

        pointer_first_label = str(pointer_first).replace(str(alt_first),str(num_alt1))
        pointer_second_label = str(pointer_second).replace(str(alt_second),str(num_alt2))
        pointer_third_label = str(pointer_third).replace(str(alt_third),str(num_alt3))
        pointer_first_medals = str(pointer_first).replace(str(alt_first),str(num_alt1m))
        pointer_second_medals = str(pointer_second).replace(str(alt_second),str(num_alt2m))
        pointer_third_medals = str(pointer_third).replace(str(alt_third),str(num_alt3m))

        print (pointer_first," ",pointer_second," ",pointer_third)

        coord_to_kml_first = coord_to_kml_dict[1]["first"]
        coord_to_kml_second = coord_to_kml_dict[1]["second"]
        coord_to_kml_third = coord_to_kml_dict[1]["third"]

        flag_first = "img/flags/"+str(values[0]).replace(" ","")+".png"
        flag_second = "img/flags/"+str(values[2]).replace(" ","")+".png"
        flag_third = "img/flags/"+str(values[4]).replace(" ","")+".png"

        #------ Little cylinders.. every country number of separated medals. Bucle 3 voltes -------
        i = 1 #i=1 first, i=2, second i=3, third
        while i<=3:
            coordinates_medals = {}
            if i == 1:
                coordinates_medals["lat"] = float(str(pointer_first).split(",")[1])
                coordinates_medals["lng"] = float(str(pointer_first).split(",")[0])

                values_medals1 = self.getValues_countryName(self.data_set.medalTable,"medals",i)

                data_dict_medals = {}
                data_dict_medals["name"] = "cylinder_medals"
                data_dict_medals["description"] = values_medals1
                data_dict_medals["coordinates"] = coordinates_medals
                data_dict_medals["extra"] = "medals"

                cylinders_medals = CylindersKml("",data_dict_medals)
                coord_to_kml_dict_medals = cylinders_medals.makeKML()

                pointer_golden1 = coord_to_kml_dict_medals[0]["golden"]
                pointer_silver1 = coord_to_kml_dict_medals[0]["silver"]
                pointer_bronze1 = coord_to_kml_dict_medals[0]["bronze"]

                coord_to_kml_golden1 = coord_to_kml_dict_medals[1]["golden"]
                coord_to_kml_silver1 = coord_to_kml_dict_medals[1]["silver"]
                coord_to_kml_bronze1 = coord_to_kml_dict_medals[1]["bronze"]

            elif i == 2:
                coordinates_medals["lat"] = float(str(pointer_second).split(",")[1])
                coordinates_medals["lng"] = float(str(pointer_second).split(",")[0])

                values_medals2 = self.getValues_countryName(self.data_set.medalTable,"medals",i)

                data_dict_medals = {}
                data_dict_medals["name"] = "cylinder_medals"
                data_dict_medals["description"] = values_medals2
                data_dict_medals["coordinates"] = coordinates_medals
                data_dict_medals["extra"] = "medals"

                cylinders_medals = CylindersKml("",data_dict_medals)
                coord_to_kml_dict_medals = cylinders_medals.makeKML()

                pointer_golden2 = coord_to_kml_dict_medals[0]["golden"]
                pointer_silver2 = coord_to_kml_dict_medals[0]["silver"]
                pointer_bronze2 = coord_to_kml_dict_medals[0]["bronze"]

                coord_to_kml_golden2 = coord_to_kml_dict_medals[1]["golden"]
                coord_to_kml_silver2 = coord_to_kml_dict_medals[1]["silver"]
                coord_to_kml_bronze2 = coord_to_kml_dict_medals[1]["bronze"]

            elif i == 3:

                coordinates_medals["lat"] = float(str(pointer_third).split(",")[1])
                coordinates_medals["lng"] = float(str(pointer_third).split(",")[0])

                values_medals3 = self.getValues_countryName(self.data_set.medalTable,"medals",i)

                data_dict_medals = {}
                data_dict_medals["name"] = "cylinder_medals"
                data_dict_medals["description"] = values_medals3
                data_dict_medals["coordinates"] = coordinates_medals
                data_dict_medals["extra"] = "medals"

                cylinders_medals = CylindersKml("",data_dict_medals)
                coord_to_kml_dict_medals = cylinders_medals.makeKML()

                pointer_golden3 = coord_to_kml_dict_medals[0]["golden"]
                pointer_silver3 = coord_to_kml_dict_medals[0]["silver"]
                pointer_bronze3 = coord_to_kml_dict_medals[0]["bronze"]

                coord_to_kml_golden3 = coord_to_kml_dict_medals[1]["golden"]
                coord_to_kml_silver3 = coord_to_kml_dict_medals[1]["silver"]
                coord_to_kml_bronze3 = coord_to_kml_dict_medals[1]["bronze"]

            i = i + 1

        alt_golden1 = str(pointer_golden1).split(",")[2]
        alt_silver1 = str(pointer_silver1).split(",")[2]
        alt_bronze1 = str(pointer_bronze1).split(",")[2]
        alt_golden2 = str(pointer_golden2).split(",")[2]
        alt_silver2 = str(pointer_silver2).split(",")[2]
        alt_bronze2 = str(pointer_bronze2).split(",")[2]
        alt_golden3 = str(pointer_golden3).split(",")[2]
        alt_silver3 = str(pointer_silver3).split(",")[2]
        alt_bronze3 = str(pointer_bronze3).split(",")[2]

        num_alt_golden1 = float(alt_golden1)/3.0
        num_alt_silver1 = float(alt_silver1)/3.0
        num_alt_bronze1 = float(alt_bronze1)/3.0
        num_alt_golden2 = float(alt_golden2)/3.0
        num_alt_silver2 = float(alt_silver2)/3.0
        num_alt_bronze2 = float(alt_bronze2)/3.0
        num_alt_golden3 = float(alt_golden3)/3.0
        num_alt_silver3 = float(alt_silver3)/3.0
        num_alt_bronze3 = float(alt_bronze3)/3.0

        pointer_golden1_label = str(pointer_golden1).replace(str(alt_golden1),str(num_alt_golden1))
        pointer_silver1_label = str(pointer_silver1).replace(str(alt_silver1),str(num_alt_silver1))
        pointer_bronze1_label = str(pointer_bronze1).replace(str(alt_bronze1),str(num_alt_bronze1))
        pointer_golden2_label = str(pointer_golden2).replace(str(alt_golden2),str(num_alt_golden2))
        pointer_silver2_label = str(pointer_silver2).replace(str(alt_silver2),str(num_alt_silver2))
        pointer_bronze2_label = str(pointer_bronze2).replace(str(alt_bronze2),str(num_alt_bronze2))
        pointer_golden3_label = str(pointer_golden3).replace(str(alt_golden3),str(num_alt_golden3))
        pointer_silver3_label = str(pointer_silver3).replace(str(alt_silver3),str(num_alt_silver3))
        pointer_bronze3_label = str(pointer_bronze3).replace(str(alt_bronze3),str(num_alt_bronze3))
        #cylinders = CylindersKml("cylinders_kml","Hola")
        #latlonaltcircle = cylinders.newCylinder("cylinder name", "cylinder description", self.data_set.longitude, self.data_set.latitude, "")

        olympic_game_doc = KML.kml(
                        KML.Document(
                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('3.5'),
                                    KML.Icon(
                                        KML.hide(True)
                                    ),
                                ),
                                KML.LabelStyle(
                                    KML.color("FF4CBB17"),
                                    KML.scale(2.5)
                                ),
                                id="style_labelJJOO"
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('3.5'),
                                    KML.Icon(
                                        KML.href("img/"+str(self.data_set.year)+" Summer Olympics.png")
                                    ),
                                ),
                                id="style_iconJJOO"
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_first)
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
                                id="style_first",
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_second)
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
                                id="style_second",
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_third)
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
                                id="style_third",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("ffffeef4"),
                                    KML.scale(2.5)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_medals_label",
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_first)
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
                                id="style_golden",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("ffffeef4"),
                                    KML.scale(2)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_first_label",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("FF4CBB17"),
                                    KML.scale(1.75)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_first_medals",
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_second)
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
                                id="style_silver",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("ffffeef4"),
                                    KML.scale(2)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_second_label",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("FF4CBB17"),
                                    KML.scale(1.75)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_second_medals",
                            ),

                            KML.Style(
                                KML.IconStyle(
                                    KML.scale('4.0'),
                                    KML.Icon(
                                        KML.href(flag_third)
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
                                id="style_bronze",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("ffffeef4"),
                                    KML.scale(2)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_third_label",
                            ),

                            KML.Style(
                                KML.LabelStyle(
                                    KML.color("FF4CBB17"),
                                    KML.scale(1.75)
                                ),
                                KML.Icon(
                                    KML.hide(True)
                                ),
                                id="style_third_medals",
                            ),

                            KML.Folder(
                                KML.name('Features'),
                                id='features',
                            ),
                    )
                )

        # fly to the data
        olympic_game_doc.Document.Folder.append(
            GX.FlyTo(
                GX.duration(6),
                GX.flyToMode("bounce"),
                KML.LookAt(
                    KML.longitude(float(self.data_set.longitude)),
                    KML.latitude(float(self.data_set.latitude)),
                    KML.altitude(0),
                    KML.heading(-55),
                    KML.tilt(65),
                    KML.name((self.data_set.hostCity).upper()),
                    KML.range(70000),
                    KML.altitudeMode("relativeToGround"),
                )
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(self.data_set.hostCity+" "+str(self.data_set.year)),
                KML.styleUrl('#{0}'.format("style_labelJJOO")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(self.data_set.longitude),
                        lat=float(self.data_set.latitude),
                        alt=25000,
                    )
                    )
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_iconJJOO")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates("{lon},{lat},{alt}".format(
                        lon=float(self.data_set.longitude),
                        lat=float(self.data_set.latitude),
                        alt=26500,
                    )
                    )
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values[0]).upper()),
                KML.styleUrl('#{0}'.format("style_first_label")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_first_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals1[1])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_golden1_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals1[2])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_silver1_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals1[3])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_bronze1_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals2[1])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_golden2_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals2[2])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_silver2_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals2[3])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_bronze2_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals3[1])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_golden3_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals3[2])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_silver3_label),
                ),
            ),
        ),
        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values_medals3[3])),
                KML.styleUrl('#{0}'.format("style_medals_label")),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_bronze3_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name("Total medals: "+str(values[1])),
                KML.styleUrl('#{0}'.format("style_first_medals")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("absolute"),
                    KML.coordinates(pointer_first_medals),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_first")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("absolute"),
                    KML.coordinates(pointer_first),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_first")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_first),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_golden")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_golden1),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_silver")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_silver1),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_bronze")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_bronze1),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_golden")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_golden2),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_silver")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_silver2),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_bronze")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_bronze2),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_golden")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_golden3),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_silver")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_silver3),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_bronze")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_bronze3),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values[2]).upper()),
                KML.styleUrl('#{0}'.format("style_second_label")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_second_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name("Total medals: "+str(values[3])),
                KML.styleUrl('#{0}'.format("style_second_medals")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_second_medals),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_second")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_second),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_second")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_second),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name(str(values[4]).upper()),
                KML.styleUrl('#{0}'.format("style_third_label")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_third_label),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.name("Total medals: "+str(values[5])),
                KML.styleUrl('#{0}'.format("style_third_medals")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_third_medals),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_third")),
                KML.Point(
                    KML.extrude(0),
                    KML.altitudeMode("relativeToGround"),
                    KML.coordinates(pointer_third),
                ),
            ),
        ),

        olympic_game_doc.Document.Folder.append(
            KML.Placemark(
                KML.styleUrl('#{0}'.format("style_third")),
                KML.MultiGeometry(
                    KML.Polygon(
                        KML.extrude(0),
                        KML.altitudeMode("absolute"),
                        KML.outerBoundaryIs(
                            KML.LinearRing(
                                KML.coordinates(coord_to_kml_third),
                            ),
                        ),
                    ),
                ),
            ),
        ),

        outfile = open(os.path.join("static/", self.kml_name+".kml"),"w+")
        outfile.write(etree.tostring(olympic_game_doc, encoding="unicode"))
        outfile.close()

        return outfile

    def set_color(self, color):
        if color == "Yellow":
            return simplekml.Color.yellow
        if color == "Red":
            return simplekml.Color.red
        if color == "Green":
            return simplekml.Color.green
        if color == "Blue":
            return simplekml.Color.blue
