from math import cos,sin,pi

class Track:
    trackID = 0
    agentType = "Unknown"
    vehicleLength = 0
    vehicleWidth = 0
    # dataLength = 0
    # frameID = []
    timeStamps = []
    x = []
    y = []
    vx = []
    vy = []
    heading = []

    def __init__(self,trackData):
        self.trackID = trackData.track_id
        self.agentType = trackData.agent_type
        self.vehicleLength = trackData.length
        self.vehicleWidth = trackData.width

        # 数组必须清零重置，否则会覆盖
        self.timeStamps = []
        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.heading = []
        self.longitudinal_vel = []
        self.lateral_vel = []
        self.angular_vel = []
        self.radius = []
        
        for motionState in trackData.motion_states:
            self.x.append(trackData.motion_states[motionState].x)
            self.y.append(trackData.motion_states[motionState].y)
            self.vx.append(trackData.motion_states[motionState].vx)
            self.vy.append(trackData.motion_states[motionState].vy)
            self.heading.append(trackData.motion_states[motionState].psi_rad)
            self.timeStamps.append(trackData.motion_states[motionState].time_stamp_ms)

        for timeStamp in range(len(self.timeStamps)):
            self.longitudinal_vel.append(self.vx[timeStamp]*cos(self.heading[timeStamp])+self.vy[timeStamp]*sin(self.heading[timeStamp]))
            self.lateral_vel.append(self.vy[timeStamp]*cos(self.heading[timeStamp])-self.vx[timeStamp]*sin(self.heading[timeStamp]))
            self.angular_vel.append(self.heading[min(timeStamp+1,len(self.timeStamps)-1)]-self.heading[timeStamp])
            if self.angular_vel[timeStamp] == 0:
                self.radius.append(8000)
            else:
                if self.longitudinal_vel[timeStamp] == 0:
                    if timeStamp == 0:
                        self.radius.append(8000)
                    else:
                        self.radius.append(self.radius[timeStamp-1])
                else:
                    self.radius.append(min(8000,self.longitudinal_vel[timeStamp]/self.angular_vel[timeStamp]))
           

   
    def displayBasic(self):
        print("TrackID = ", self.trackID,", AgentType = ", self.agentType,
              ", VehicleLength = ", self.vehicleLength,
              ", VehicleWidth = ", self.vehicleWidth)

    def displayMotionStatus(self,timeStamp):
        print("TrackID = ", self.trackID, "; TimeStamp = ", self.timeStamps[timeStamp], 
                                            " x = " ,self.x[timeStamp] ,
                                            " y = " , self.y[timeStamp] , 
                                            " vx = " , self.vx[timeStamp] , 
                                            " vy = " , self.vy[timeStamp] ,
                                            " heading = " , self.heading[timeStamp],
                                            " longitudinal_vel = ", self.longitudinal_vel[timeStamp],
                                            " lateral_vel = ", self.lateral_vel[timeStamp],
                                            " angular_vel = ", self.angular_vel[timeStamp],
                                            " radius = ", self.radius[timeStamp])

    def show(self):
        self.displayBasic()
        for timeStamp in range(len(self.timeStamps)):
            self.displayMotionStatus(timeStamp)