from datetime import datetime

class Description :
    def __init__(self,weekdayRestriction,timeIntervalRestriction) :
        self.weekdayRestriction=weekdayRestriction
        self.timeIntervalRestriction=timeIntervalRestriction
    #----------------------------------------------------------------------------
    def numberOfWeekDays(self) :
        return len(self.weekdayRestriction)
    def duration(self) :
        return abs((datetime(2015,2,22,self.timeIntervalRestriction[1].hour,self.timeIntervalRestriction[1].minute,self.timeIntervalRestriction[1].second)-datetime(2015,2,22,self.timeIntervalRestriction[0].hour,self.timeIntervalRestriction[0].minute,self.timeIntervalRestriction[0].second)).total_seconds())
    #----------------------------------------------------------------------------
    def compareCannonicOrder(self,other,actualAtt) :
        if (actualAtt==1) : return len(set(self.weekdayRestriction) & set(other.weekdayRestriction))==len(self.weekdayRestriction)
        return True
    #----------------------------------------------------------------------------
    def isTrajectoryIn(self,trajectory) :
        return (trajectory.weekday in self.weekdayRestriction and self.timeIntervalRestriction[0]<=trajectory.time<=self.timeIntervalRestriction[1])
    #----------------------------------------------------------------------------
    def __rand__(self,other) :
        if (other.__class__.__name__=="Trajectory") :
            W=set(self.weekdayRestriction[:])
            T=self.timeIntervalRestriction[:]
            W.add(other.weekday)
            W=sorted(W)
            T[0]=min(T[0],other.time)
            T[1]=max(T[1],other.time)
        else :
            W=sorted(set(self.weekdayRestriction) & set(other.weekdayRestriction))
            T=self.timeIntervalRestriction[:]
            T[0]=min(T[0],other.timeIntervalRestriction[0])
            T[1]=max(T[1],other.timeIntervalRestriction[1])
        return Description(W,T)

    def __iand__(self,other) :
        return self.__rand__(other)
    #----------------------------------------------------------------------------
    def restrictWeekdays(self,p) :
        pNewDescriptionWeekdays=self.weekdayRestriction[:]
        pNewDescriptionWeekdays.pop(len(pNewDescriptionWeekdays)-1-p)
        return Description(pNewDescriptionWeekdays,self.timeIntervalRestriction[:])

    def restrictRightTimeInterval(self,sortedHours,hoursValueIndexMap) :
        return Description(self.weekdayRestriction[:],[self.timeIntervalRestriction[0],sortedHours[hoursValueIndexMap[str(self.timeIntervalRestriction[1])]-1]])

    def restrictLeftTimeInterval(self,sortedHours,hoursValueIndexMap) :
        return Description(self.weekdayRestriction[:],[sortedHours[hoursValueIndexMap[str(self.timeIntervalRestriction[0])]+1],self.timeIntervalRestriction[1]])
    #----------------------------------------------------------------------------
    def __str__(self) :
        return "<"+str(self.weekdayRestriction)+",["+str(self.timeIntervalRestriction[0])+","+str(self.timeIntervalRestriction[1])+"]>"
