from Position import Position
from geopy.geocoders import Nominatim

class Poi(Position) :
    def __init__(self,poiId,longitude,latitude,visits=[]) :
        self.id=poiId
        Position.__init__(self,longitude,latitude)
        self.visits=visits[:]
        self.accumulatedStayTime=sum([visit.duration() for visit in self.visits])

    def addVisit(self,visit) :
        visit.poiId=self.id
        self.visits.append(visit)
        self.accumulatedStayTime+=visit.duration()

    def setVisits(self,visits) :
        self.visits=[]
        self.accumulatedStayTime=0
        for visit in visits : self.addVisit(visit)
        
    def updateId(self,newId) :
        self.id=newId
        for visit in self.visits : visit.poiId=newId
        
    def address(self):
        geolocator = Nominatim()
        location = geolocator.reverse("{0}, {1}".format(self.latitude(),self.longitude()))
        return location.address
    
    def __str__(self) :
        return "POI {0} : {1} \n number of visit : {2} \n accumulatedStayTime : {3} h".format(self.id,self.position,len(self.visits),round(self.accumulatedStayTime/3600,2))

    
