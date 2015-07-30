import math
import numpy as np

class Position :
    def __init__(self,longitude,latitude) :
        self.position=np.array([longitude,latitude])

    def longitude(self) :
        return self.position[0]

    def latitude(self) :
        return self.position[1]

    def distance(self,other) :
        """
        return distance between two points in earth in meter
        """
        if (self.position[1]==other.position[1] and self.position[0]==other.position[0]) : return 0
        degrees_to_radians = math.pi/180.0

        phi1 = (90.0 - self.position[1])*degrees_to_radians
        phi2 = (90.0 - other.position[1])*degrees_to_radians
         
        theta1 = self.position[0]*degrees_to_radians
        theta2 = other.position[0]*degrees_to_radians
         
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))

        if (cos>1) : cos=1
        elif (cos<-1) : cos=-1
    
        arc = math.acos( cos )
        r=6378137

        return round(r*arc,4)

    def distanceP(self,other,p=2) :
        """
        return the p-minkowski distance between the two points
        """
        return ((self.longitude()-other.longitude())**p+(self.latitude()-other.latitude())**p)**(1./p)

    def bearing(self,other) :
        degrees = 180 / math.pi
        dLon = other.longitude() - self.longitude()
        y = math.sin(dLon) * math.cos(other.latitude())
        x = math.cos(self.latitude())*math.sin(other.latitude()) - math.sin(self.latitude())*math.cos(other.latitude())*math.cos(dLon)
        brng = math.atan2(y, x)*degrees
        if (brng<0) : brng+=360
        return brng

    def __add__(self,other) :
        return Position(self.longitude()+other.longitude(),self.latitude()+other.latitude())

    def __sub__(self,other) :
        return self.distance(other)

    def __div__(self,other) :
        return Position(float(self.longitude())/other,float(self.latitude())/other)

    def __mul__(self,other) :
        return Position(self.longitude()*other,self.latitude()*other)

    def __str__(self) :
        return str(self.position)
