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
        
        for motionState in trackData.motion_states:
            self.x.append(trackData.motion_states[motionState].x)
            self.y.append(trackData.motion_states[motionState].y)
            self.vx.append(trackData.motion_states[motionState].vx)
            self.vy.append(trackData.motion_states[motionState].vy)
            self.heading.append(trackData.motion_states[motionState].psi_rad)
            self.timeStamps.append(trackData.motion_states[motionState].time_stamp_ms)
   
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
                                            " heading = " , self.heading[timeStamp])

    def show(self):
        self.displayBasic()
        for timeStamp in range(len(self.timeStamps)):
            self.displayMotionStatus(timeStamp)