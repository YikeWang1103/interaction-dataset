import os
import numpy as np
import math
import matplotlib.pyplot as plt

import lanelet2
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, LineString2d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d
from lanelet2.projection import UtmProjector
from utils import map_vis_lanelet2

maps_dir = "../../maps"
lanelet_map_ending = ".osm"
scenario_name = "DR_USA_Intersection_EP0"
lanelet_map_file = maps_dir + "/" + scenario_name + lanelet_map_ending

lat_origin = 0.  # origin is necessary to correctly project the lat lon values in the osm file to the local
lon_origin = 0.  # coordinates in which the tracks are provided; we decided to use (0|0) for every scenario

def loadMap():
    path = os.path.join(lanelet_map_file)
    projector = UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletMap, errors = lanelet2.io.loadRobust(path, projector)
    assert not errors
    return laneletMap

def calCurvature(targetLanelet):
    centerline = targetLanelet.centerline
    print("Lanelet ID = ", targetLanelet.id)
    # print(type(centerline))

    distance = 0
    deltaSlope = 0
    
    if len(centerline) > 2:
        for i in range(len(centerline)-2):
            slopeCurr = math.atan2((centerline[i+1].y - centerline[i].y),(centerline[i+1].x - centerline[i].x))
            slopeNext = math.atan2((centerline[i+2].y - centerline[i+1].y),(centerline[i+2].x - centerline[i+1].x))
            deltaSlope += (slopeNext - slopeCurr)
            print("slopeCurr = ", slopeCurr, "; slopeNext = ", slopeNext, "; deltaSlope = ", deltaSlope)
            distance  += math.sqrt((centerline[i+1].x - centerline[i].x)**2 + (centerline[i+1].y - centerline[i].y)**2)

        if distance == 0:
            curvature = 0
        else: 
            curvature = deltaSlope / distance
    else:
        curvature = 0

    print("curvature = ", curvature)
    if curvature == 0:
        print("radius = Inf")
    else:
        radius = 1/curvature
        print("radius = ", radius)

    return curvature

def addCurvature2Map(laneletMap):
    plotMap(laneletMap)
    plt.draw()
    for lanelet in laneletMap.laneletLayer:
        curvature = calCurvature(lanelet)
        laneletID = lanelet.id
        plotCenterline(laneletMap, laneletID)
    
    plt.show()

def plotMap(laneletMap):
    fig, axes = plt.subplots(1,1)
    map_vis_lanelet2.draw_lanelet_map(laneletMap, axes)


def plotCenterline(laneletMap, laneletID):
    centerline = laneletMap.laneletLayer.get(laneletID).centerline
    x = []
    y = []
    type_dict = dict(color="red", linewidth=1, zorder=10, dashes=[2, 5])
    for i in range(len(centerline)):
        x.append(centerline[i].x)
        y.append(centerline[i].y)

    plt.plot(x,y,**type_dict)
    plt.draw()

def plotRoute(laneletID):
    projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletMap = lanelet2.io.load(lanelet_map_file, projector)
    centerline = laneletMap.laneletLayer.get(laneletID).centerline
    x = []
    y = []
    # type_dict = dict(color="red", linewidth=1, zorder=10, dashes=[2, 5])
    for i in range(len(centerline)):
        x.append(centerline[i].x)
        y.append(centerline[i].y)

    plt.plot(x,y,'ro')
    plt.draw()
    plt.show()

if __name__ == "__main__":
    laneletMap = loadMap()
    addCurvature2Map(laneletMap)

    # plotRoute(30058)

