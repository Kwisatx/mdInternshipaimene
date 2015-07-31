class Visit :
    def __init__(self,poiId,arrival,departure) :
        self.poiId=poiId
        self.arrival=arrival
        self.departure=departure

    def __str__(self) :
        return "visit of poi {0} from {1} to {2}".format(self.poiId,str(self.arrival),str(self.departure))

    def duration(self) :
        return (self.departure-self.arrival).total_seconds()
