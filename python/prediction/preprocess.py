import json
import xlrd, xlwt
import csv
import lanelet2
from utils import map_vis_lanelet2
import matplotlib.pyplot as plt


import os
import numpy as np
import math

from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, LineString2d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d
from lanelet2.projection import UtmProjector


maps_dir = "../../maps"
lanelet_map_ending = ".osm"
scenario_name = "DR_USA_Intersection_EP0"

lanelet_map_file = maps_dir + "/" + scenario_name + lanelet_map_ending

lat_origin = 0.  
lon_origin = 0. 


class Track:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.heading = 0
        self.curvature = 0 

def tutorial_1():
    p = Point3d(getId(), 0, 0, 0)
    print("ID = ", p.id)
    p2 = lanelet2.geometry.to2D(p)
    p2.y = 1
    print("p2 = ", p2)
    print("p = ", p)
    print("Distance = ",lanelet2.geometry.distance(lanelet2.geometry.to2D(p), p2))
    assert lanelet2.geometry.distance(Point2d(getId(),0,0), p2) == 1

def plotMap():
    projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletmap = lanelet2.io.load(lanelet_map_file, projector)
    fig, axes = plt.subplots(1,1)
    map_vis_lanelet2.draw_lanelet_map(laneletmap, axes)
    # plt.show()

def loadMap():
    path = os.path.join(lanelet_map_file)
    projector = UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletMap, errors = lanelet2.io.loadRobust(path, projector)
    assert not errors
    return laneletMap

def getLaneletCandidates(basicPoint2d, laneletMap, numOfCandidates):
    nearestLanelets = laneletMap.laneletLayer.nearest(basicPoint2d,numOfCandidates)
    laneletCandidates = []
    for i in range(numOfCandidates):
        if(lanelet2.geometry.inside(nearestLanelets[i],basicPoint2d)):
            print("BasicPoint2d(",basicPoint2d.x,",",basicPoint2d.y,") is inside of lanelet ID = ",nearestLanelets[i].id)
            laneletCandidates.append(nearestLanelets[i])
    return laneletCandidates

def calCurvature(targetLanelet):
    centerline = targetLanelet.centerline
    print("Lanelet ID = ", targetLanelet.id)
    print(type(centerline))

    # centerline = lineStringProj(centerline)

    distance = 0
    deltaSlope = 0
    for i in range(round(len(centerline)/2)):
        slopeCurr = math.atan2((centerline[i+1].y - centerline[i].y),(centerline[i+1].x - centerline[i].x))
        slopeNext = math.atan2((centerline[i+2].y - centerline[i+1].y),(centerline[i+2].x - centerline[i+1].x))
        deltaSlope += (slopeNext - slopeCurr)
        print("deltaSlope = ", deltaSlope)
        distance  += math.sqrt((centerline[i+1].x - centerline[i].x)**2 + (centerline[i+1].y - centerline[i].y)**2)

    curvature = deltaSlope / distance
    print("curvature = ", curvature)
    radius = 1/curvature
    print("radius = ", radius)

    x = []
    y = []
    type_dict = dict(color="red", linewidth=1, zorder=10, dashes=[2, 5])
    for i in range(len(centerline)-5):
        x.append(centerline[i].x)
        y.append(centerline[i].y)
    # plt.subplots(1,1)
    plt.plot(x,y,**type_dict)
    plt.show()
    # print("Curvature02 = ", LineString3d.curvature2d(centerline[0],centerline[3],centerline[5]))

def pointProj(point2D,trackInfo):
    point2D_ = Point3d()
    x = point2D.x - trackInfo.x
    y = point2D.y - trackInfo.y
    theta = trackInfo.heading

    point2D_.x = -1*(y*math.cos(theta) - x*math.sin(theta))
    point2D_.y = x*math.cos(theta) + y*math.sin(theta)
    print("point2D_.x = ", round(point2D_.x,7), "; point2D_.y = ", round(point2D_.y,7))
    return point2D_

def lineStringProj(lineString):
    trackInfo = Track()
    trackInfo.x = 988.141
    trackInfo.y = 983.852
    trackInfo.heading = -0.082
    points = []
    for i in range(len(lineString)):
        points.append(pointProj(lineString[i],trackInfo))
    
    lineString_ = LineString2d(getId(),points)

    return lineString_

if __name__ == "__main__":
    # plt.ion()
    # plt.show()
    plotMap()
    # tutorial_1()

    laneletMap = loadMap()
    basicPoint2d = BasicPoint2d(996.9, 998.1)
    numOfCandidates = 10
    laneletCandidates = getLaneletCandidates(basicPoint2d, laneletMap, numOfCandidates)
    print("The length of laneletCandidates = ",len(laneletCandidates))
    calCurvature(laneletCandidates[0])

    # while(1):
    #     plt.draw()
    #     plt.pause(0.1)
    # pointProj()







