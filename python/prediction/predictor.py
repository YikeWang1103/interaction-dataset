import os
import argparse
import lanelet2
from lanelet2.core import BasicPoint2d
from utils import map_vis_lanelet2
from utils import tracks_vis

import matplotlib.pyplot as plt
import matplotlib.patches
import numpy as np
from track import Track
from importData import importTrackData,importMapData
from plotter import plotParticle,plotAgents,plotScenario
from particle import Particle, addParticles
import pgmpy as bayesianNetwork
import math


mapFolder = "../../dataset/INTERACTION-Dataset-DR-v1_1/maps/"
DataFolder = "../../dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/"
targetFile = "../../dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP0/vehicle_tracks_000.csv"

# trackCandidate = [12,13]
# trackCandidate = [12]
trackCandidate = [13]
particleNumber = 10

def determineLanelets(basicPoint2d, laneletMap, numOfCandidates=10):
    nearestLanelets = laneletMap.laneletLayer.nearest(basicPoint2d,numOfCandidates)
    laneletCandidates = []

    for i in range(numOfCandidates):
        if(lanelet2.geometry.inside(nearestLanelets[i],basicPoint2d)):
            # print("BasicPoint2d(",basicPoint2d.x,",",basicPoint2d.y,") is inside of lanelet ID = ",nearestLanelets[i].id)
            laneletCandidates.append(nearestLanelets[i])

    return laneletCandidates


def determineRoutes(particles,laneletMap):
    route_candidates = []

    for particleID in range(len(particles[0])):
        particlePos = BasicPoint2d(particles[0][particleID].x, particles[0][particleID].y)
        laneletCandidates = determineLanelets(particlePos, laneletMap)
        for laneletID in range(len(laneletCandidates)):
            if len(route_candidates) == 0:
                route_candidates.append(laneletCandidates[laneletID])
            else:
                checkDuplicate = False
                for routeID in range(len(route_candidates)):
                    if laneletCandidates[laneletID].id == route_candidates[routeID].id:
                        checkDuplicate = True
                        break    
                
                if checkDuplicate == False:
                    route_candidates.append(laneletCandidates[laneletID])

    return route_candidates
     
def trajectoryPredictor(agents,particles,laneletMap):
    trajectory = []
    route_candidates = determineRoutes(particles,laneletMap)
    



    return trajectory

def getLaneletSuccessor(agents,laneletMap,timeStamp):
    laneletSuccessor = []
    traffic_rules = lanelet2.traffic_rules.create(lanelet2.traffic_rules.Locations.Germany,
                                                  lanelet2.traffic_rules.Participants.Vehicle)

    graph = lanelet2.routing.RoutingGraph(laneletMap,traffic_rules)

    for agentID in range(len(agents)):
        agentPos = BasicPoint2d(agents[agentID].x[timeStamp], agents[agentID].y[timeStamp])
        laneletCandidate = determineLanelets(agentPos, laneletMap)
        successor = []
        for candidateID in range(len(laneletCandidate)):
            successor.append(graph.following(laneletCandidate[candidateID]))
            for successorID in range(len(graph.following(laneletCandidate[candidateID]))):
                print("Agent ID = ", agents[agentID].trackID, 
                    "; lanelet Candidate ID = ", laneletCandidate[candidateID].id,
                    "; lanelet Successor ID = ", graph.following(laneletCandidate[candidateID])[successorID].id)
        laneletSuccessor.append(successor)

    return laneletSuccessor

def squeezeLaneletSuccessor(laneletSuccessors):
    squeezedLaneletSuccessors = []

    for agentID in range(len(laneletSuccessors)):
        tempLaneletSuccessor = []
        for laneletID in range(len(laneletSuccessors[agentID])):
            for successorID in range(len(laneletSuccessors[agentID][laneletID])):
                tempLaneletSuccessor.append(laneletSuccessors[agentID][laneletID][successorID])
                tempLaneletSuccessor = list(set(tempLaneletSuccessor))
            
        squeezedLaneletSuccessors.append(tempLaneletSuccessor)

    # for agentID in range(len(squeezedLaneletSuccessor)):
    #     for successorID in range(len(squeezedLaneletSuccessor[agentID])):
    #             print("Lanelet successor ID = ", squeezedLaneletSuccessor[agentID][successorID])

    return squeezedLaneletSuccessors

def calculateRouteIntentionProb(agents,squeezedLaneletSuccessors,timeStamp):
    routeIntentionProb = []

    for agentID in range(len(squeezedLaneletSuccessors)):
            routeIntention = []
            radius_list = []
            agentRadius = agents[agentID].radius[timeStamp]
            # agentRadius = 800
            print("AgentRadius = ",agentRadius)
            
            for successorID in range(len(squeezedLaneletSuccessors[agentID])):
                targetLanelet = squeezedLaneletSuccessors[agentID][successorID]
                radius_list.append(1/float(targetLanelet.attributes["curvature"]))
            
            print("radius_list = ",radius_list)
            numSuccessor = len(radius_list)
            radius_diff = [math.log(abs(agentRadius-i),10)**2 for i in radius_list] 
            dem = sum(radius_diff)

            iter_list = radius_diff + radius_diff[0:-1]
            print("radius_diff = ", radius_diff)

            for iter in range(numSuccessor):
                routeIntention.append(1-iter_list[iter]/dem)

            print("routeIntention = ", routeIntention)

            routeIntentionProb.append(routeIntention)

    return routeIntentionProb


def createBayesianNetwork(agents,laneletMap,timeStamp):
    laneletSuccessors = getLaneletSuccessor(agents,laneletMap,timeStamp)
    squeezedLaneletSuccessors = squeezeLaneletSuccessor(laneletSuccessors)
    routeIntentionProb = calculateRouteIntentionProb(agents,squeezedLaneletSuccessors,timeStamp)



    network = []


    return network

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("scenarioFolder", type=str, help="Path of target dataset", default="DR_USA_Intersection_EP0", nargs="?")
    args = parser.parse_args()
    scenarioFolder = args.scenarioFolder

    # extract track information
    tracks = importTrackData(targetFile)

    agents = []
    for i in range(len(trackCandidate)):
        agents.append(tracks[trackCandidate[i]-1])

    # extract map information
    mapDataPath = mapFolder + scenarioFolder + ".osm" 
    # print("mapDataPath = ", mapDataPath)
    lat_origin = 0.
    lon_origin = 0.
    laneletMap = importMapData(mapDataPath, lat_origin, lon_origin)


    # trajectory prediction of track candidates
    # timeStamp = 60
    for timeStamp in range(136):
    # particles = addParticles(agents,particleNumber,timeStamp)
    # agentsTrajectory = trajectoryPredictor(agents,particles,laneletMap)
        bayesianNetowrk = createBayesianNetwork(agents,laneletMap,timeStamp)


    # for agentID in range(len(particles)):
    #     print("Agent ", agentID, ":")
    #     for particleID in range(len(particles[agentID])):
    #         print("Particle: x = ",particles[agentID][particleID].x, ", y = ",particles[agentID][particleID].y)
            

    # plot the scenarios
    # plotScenario(laneletMap,agents,particles,timeStamp)