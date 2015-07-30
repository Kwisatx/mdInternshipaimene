import os
from binascii import hexlify
from datetime import datetime
from math import isnan
import numpy as np
import matplotlib.pyplot as plt
from Utils.Event import Event

#---------------------------- Utilitues -------------------------------------------------------------#
def getDateTime(strDateTime) :
    try :
        return datetime.strptime(strDateTime,"%Y-%m-%dT%H:%M:%SZ")
    except ValueError :
        return datetime.strptime(strDateTime,"%Y-%m-%dT%H:%M:%S")
#----------------------------------------------------------------------------------------------------#

#---------------------------- Generator -------------------------------------------------------------#
def getCSVLines(linesTraces) :
    begin=True
    lines=linesTraces[:]
    lines.pop(0)
    for line in lines:
        line = line.strip().split(";")
        yield line
#----------------------------------------------------------------------------------------------------#
    
#---------------------------- Reader Class ----------------------------------------------------------#
class MobilityTraceReader :
    def __init__(self,linesTraces) :
        self.linesTraces=linesTraces
    #------------------- Read -----------------------------------------------------------------------#
    def read(self) :
        """
        CSV columns : 
        0 : recorder_at
        1 : longitude
        2 : latitude
        """
        lines=getCSVLines(self.linesTraces)
        events=[]
        for line in lines:
            if (line[1]=="?") :
                if (not events) : continue
                line[1]=events[-1].longitude()
                line[2]=events[-1].latitude()
            event=Event(getDateTime(line[0]),float(line[1]),float(line[2]))
            events.append(event)
        self.events=events

    def readWithStop(self) :
        """
        CSV columns : 
        0 : recorder_at
        1 : longitude
        2 : latitude
        3 : DIO_IGNITION
        4 : GPS_DIR
        5 : GPS_SPEED
        6 : GPRMC_VALID
        """
        lines=getCSVLines(self.linesTraces)
        events = []
        stops=[]
        for line in lines:
            if (line[1]=="?") :
                if (not events) : continue
                line[1]=events[-1].longitude()
                line[2]=events[-1].latitude()
            event=Event(getDateTime(line[0]),float(line[1]),float(line[2]))
            if (line[3]=="0") : stops.append(event)
            events.append(event)
        self.events=events
        self.stops=np.array(stops)

    def readWithPreProcessing(self,samplingTime=0,distanceMin=0,tempsMaxPerteSignal=float("inf")) :
        """
        CSV columns : 
        0 : recorder_at
        1 : longitude
        2 : latitude
        """
        lines=getCSVLines(self.linesTraces)
        events=[]
        lastEvent=None
        part=1
        for line in lines:
            if (line[2]=="?" or isnan(float(line[2]))) : continue
            event=Event(getDateTime(line[0]),float(line[1]),float(line[2]))

            if (events) : delai,distance=event - events[-1]
            else : delai,distance=float("inf"),float("inf")

            if (lastEvent) : delaiPourPerte=event.delai(lastEvent)
            elif (events) : delaiPourPerte=event.delai(events[-1]) 
            else  : delaiPourPerte=0
            
            if ((delai>=samplingTime and distance>=distanceMin) or delaiPourPerte>tempsMaxPerteSignal):
                if (delaiPourPerte>tempsMaxPerteSignal) :
                    if (lastEvent) :
                        lastEvent.part=part
                        events.append(lastEvent)
                    part+=1
                event.part=part
                events.append(event)
                lastEvent=None
            else : lastEvent=event
        self.events=events
    #------------------------------------------------------------------------------------------------------#

    #------------------- figure ---------------------------------------------------------------------------#
    def figureEvents(self) :
        longitudes=np.array([event.longitude() for event in self.events])
        latitudes=np.array([event.latitude() for event in self.events])
        plt.figure(1)
        plt.clf()
        img=plt.figure()
        plt.plot(longitudes,latitudes, 'o', markerfacecolor='k',markeredgecolor='k', markersize=1)
        importantPointsLongitude=[]
        importantPointsLatitude=[]
        try :
            importantPointsLongitude=[poi.longitude() for poi in self.stops if not isnan(poi.longitude())]
            importantPointsLatitude=[poi.latitude() for poi in self.stops if not isnan(poi.latitude())]
        except AttributeError :
            importantPointsLongitude=[]
            importantPointsLatitude=[]
        plt.plot(importantPointsLongitude,importantPointsLatitude, 'o', markerfacecolor='b',markeredgecolor='k', markersize=10)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title('Number of events : {0}, Number of Important places : {1}'.format(len(self.events),len(importantPointsLongitude)))
        #img.savefig("image.png",dpi = 500)
        return img
    #------------------------------------------------------------------------------------------------------#

