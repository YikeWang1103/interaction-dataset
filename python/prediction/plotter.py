import matplotlib.pyplot as plt
import matplotlib.patches
from utils import tracks_vis
import numpy as np
from utils import map_vis_lanelet2

def plotParticle(particles):
    print("Plotting particles!")
    for agentID in range(len(particles)):
        for partlID in range(len(particles[agentID])):
            plt.plot(particles[agentID][partlID].x,particles[agentID][partlID].y,'b.',zorder=10)

def plotAgents(agents,axes,timeStamp):
    for agentID in range(len(agents)):
        lowleft = (agents[agentID].x[timeStamp] - agents[agentID].vehicleLength / 2., 
                   agents[agentID].y[timeStamp] - agents[agentID].vehicleWidth/2.)
        lowright = (agents[agentID].x[timeStamp] + agents[agentID].vehicleLength / 2., 
                    agents[agentID].y[timeStamp] - agents[agentID].vehicleWidth / 2.)
        upright = (agents[agentID].x[timeStamp] + agents[agentID].vehicleLength / 2., 
                   agents[agentID].y[timeStamp] + agents[agentID].vehicleWidth / 2.)
        upleft = (agents[agentID].x[timeStamp] - agents[agentID].vehicleLength / 2., 
                  agents[agentID].y[timeStamp] + agents[agentID].vehicleWidth / 2.)
        polygon_pts = tracks_vis.rotate_around_center(np.array([lowleft, lowright, upright, upleft]), 
                                                      np.array([agents[agentID].x[timeStamp], agents[agentID].y[timeStamp]]), yaw=agents[agentID].heading[timeStamp])
        rect = matplotlib.patches.Polygon(polygon_pts, closed=True, zorder=5)
        axes.add_patch(rect)

def plotScenario(laneletMap,agents,particles,timeStamp):
    fig, axes = plt.subplots(1, 1)
    fig.canvas.set_window_title("Interaction Dataset Visualization")
    print("Loading map...")
    
    plotParticle(particles)
    plotAgents(agents,axes,timeStamp)
    map_vis_lanelet2.draw_lanelet_map(laneletMap, axes)
    plt.plot()
    plt.show()