import csv
import os
import lanelet2
from lanelet2.projection import UtmProjector
from utils import dataset_reader
from track import Track
import argparse
      
def importCSVData(recordedDataPath):
    csvFiles = os.listdir(recordedDataPath)
    csvData = {}
    
    for file in csvFiles:
        fileName = recordedDataPath + "/" + file
        print(fileName)

        tracks = importTrackData(fileName)
        csvData[file] = tracks

    return csvData 

def importTrackData(fileName):
    tracks = []

    if "pedestrian" in fileName:
        data_dict = dataset_reader.read_pedestrian(fileName)
    else:
        data_dict = dataset_reader.read_tracks(fileName)

    for key in data_dict.keys():
        trackData = Track(data_dict[key])
        # trackData.show()
        tracks.append(trackData)
    
    return tracks

def importMapData(mapDataPath, lat_origin, lon_origin):
    path = os.path.join(mapDataPath)
    projector = UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletMap, errors = lanelet2.io.loadRobust(path, projector)

    assert not errors

    return laneletMap

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("scenarioFolder", type=str, help="Path of target dataset", default="DR_USA_Intersection_EP0", nargs="?")
    args = parser.parse_args()
    scenarioFolder = args.scenarioFolder
    mapFolder = "../../dataset/INTERACTION-Dataset-DR-v1_1/maps/"
    mapDataPath = mapFolder + scenarioFolder + ".osm" 
    print("mapDataPath = ", mapDataPath)
    lat_origin = 0.  
    lon_origin = 0. 
    laneletMap = importMapData(mapDataPath, lat_origin, lon_origin)
    traffic_rules = lanelet2.traffic_rules.create(lanelet2.traffic_rules.Locations.Germany,
                                                  lanelet2.traffic_rules.Participants.Vehicle)
    graph = lanelet2.routing.RoutingGraph(laneletMap,traffic_rules)
    lanelet = laneletMap.laneletLayer[30028]
    for lane_ID in range(len(graph.following(lanelet))):
        print(graph.following(lanelet)[lane_ID].id)