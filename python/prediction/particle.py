import random

class Particle:
    x = 0
    y = 0
    psi_rad = 0

    def __init__(self,x_,y_,psi_rad_):
        self.x = x_
        self.y = y_
        self.psi_rad = psi_rad_

def addParticles(agents,particleNumber,timeStamp):
    particles = []
    # particlesAgent = []

    for agentID in range(len(agents)):
        particlesAgent = []
        for partlID in range(particleNumber):
            particle_x = (random.random()-0.5) * 3 + agents[agentID].x[timeStamp]
            particle_y = (random.random()-0.5) * 3 + agents[agentID].y[timeStamp]
            particle_psi_rad = random.random() * 0.1 + agents[agentID].heading[timeStamp]
            particlesAgent.append(Particle(particle_x,particle_y,particle_psi_rad))

        particles.append(particlesAgent)

    return particles