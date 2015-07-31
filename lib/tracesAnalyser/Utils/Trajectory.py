from datetime import time

class Trajectory :
    def __init__(self,visit,nextVisit) :
        daysFr=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
        
        self.date=visit.departure.date()
        self.time=visit.departure.time()

        if (time(8,0,0)<=self.time<=time(12,0,0)) : self.dayPart="matin"
        elif (time(12,0,0)<self.time<=time(19,0,0)) : self.dayPart="apres-midi"
        else : self.dayPart="nuit"

        self.weekdayNumber=self.date.weekday()
        self.weekday=daysFr[self.weekdayNumber]
        
        self.dayType="weekend" if (self.weekdayNumber in [5,6]) else "workday"

        self.classe=(visit.poiId,nextVisit.poiId)

    def __str__(self) :
        return "{0};{1};{2};{3};{4};{5}".format(str(self.date),str(self.time),self.weekday,self.dayType,self.dayPart,self.classe)
