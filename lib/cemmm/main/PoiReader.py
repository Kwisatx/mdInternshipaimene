from Utils.Visit import Visit
from Utils.Poi import Poi
from Utils.Trajectory import Trajectory
from datetime import datetime

class PoiReader :
    def __init__(self,sourcePOI,sourceVisits) :
        self.poi,self.visits=PoiReader.readAll(sourcePOI,sourceVisits)
        self.trajectories=[]
        for i in range(len(self.visits)-1) : self.trajectories.append(Trajectory(self.visits[i],self.visits[i+1]))
    #--------------------------------------------------------------------------------------------
    @staticmethod
    def readVisits(visitsLines) :
        listeVisit = []
        begin=True
        for line in visitsLines:
            if (not begin) : 
                line = line.strip().split(";")
                listeVisit.append(Visit(line[0],datetime.strptime(line[1],"%Y-%m-%d %H:%M:%S"),datetime.strptime(line[2],"%Y-%m-%d %H:%M:%S")))
            else : begin=False
        listeVisit=sorted(listeVisit,key=lambda visit : visit.arrival)
        return listeVisit
    
    @staticmethod
    def readAll(poiLines,visitsLines) :
        listeVisit=PoiReader.readVisits(visitsLines)
        begin=True
        listePOI = []
        for line in poiLines:
            if (not begin) : 
                line = line.strip().split(";")
                visits=[visit for visit in listeVisit if visit.poiId==line[0]]
                listePOI.append(Poi(line[0],float(line[1]),float(line[2]),visits))
            else : begin=False
        return listePOI,listeVisit
    #--------------------------------------------------------------------------------------------
