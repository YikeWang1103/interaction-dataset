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


mapFolder = "../../dataset/INTERACTION-Dataset-DR-v1_1/maps/"
DataFolder = "../../dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/"
targetFile = "../../dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP0/vehicle_tracks_000.csv"

# trackCandidate = [12,13]
trackCandidate = [12]
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

    print("route candidate IDs are ")
    for route_ID in range(len(route_candidates)):
        print(route_candidates[route_ID].id)

    



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
            print("lanelet Candidate ID = ", laneletCandidate[candidateID].id)
            successor.append(graph.following(laneletCandidate[candidateID]))
        laneletSuccessor.append(successor)


    for i in range(len(laneletSuccessor)):
        for j in range(len(laneletSuccessor[i])):
            for k in range(len(laneletSuccessor[i][j])):
                print("Lane let Successor = ",laneletSuccessor[i][j][k].id)

    return laneletSuccessor
            
def createBayesianNetwork(agents,laneletMap,timeStamp):
    laneletSuccessors = getLaneletSuccessor(agents,laneletMap,timeStamp)


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
    timeStamp = 60
    particles = addParticles(agents,particleNumber,timeStamp)
    bayesianNetowrk = createBayesianNetwork(agents,laneletMap,timeStamp)
    agentsTrajectory = trajectoryPredictor(agents,particles,laneletMap)

    for agentID in range(len(particles)):
        print("Agent ", agentID, ":")
        for particleID in range(len(particles[agentID])):
            print("Particle: x = ",particles[agentID][particleID].x, ", y = ",particles[agentID][particleID].y)
            

    # plot the scenarios
    plotScenario(laneletMap,agents,particles,timeStamp)