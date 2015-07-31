from Position import Position
    
class Event(Position) :
    def __init__(self,time,longitude,latitude) :
        self.time=time
        Position.__init__(self,longitude,latitude)

    def delai(self,other) :
        """
        return difference of time in seconds between the two event (in absolute value)
        """
        return abs((self.time-other.time).total_seconds())

    def __sub__(self,other) :
        """
        return both distance and difference in time 
        """
        return (self.delai(other),self.distance(other))

    def __str__(self) :
        return "({0},{1})".format(str(self.time),self.position)
