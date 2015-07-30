import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
from Utils.Poi import Poi
from Utils.Visit import Visit
from Poi_finder import Poi_finder

class SBPoiExtractor(Poi_finder) :
    def __init__(self,events,stops,distanceThres=0.0005,stayTimeThres=600,freqThres=1) :
        self.events=events
        self.stops=stops
        self.distanceThres=distanceThres
        self.stayTimeThres=stayTimeThres
        self.freqThres=freqThres
        
        Poi_finder.__init__(self,self.events)

    def getPoi(self) :
        self.poi=[]
        
        #---- Step 1 : Get events near to each stop point ---------------------------------------------------#
        associatedVisits=[]
        neighboorsServerAll=NearestNeighbors(radius=self.distanceThres, algorithm='auto',leaf_size=10)
        neighboorsServerAll.fit(np.array([event.position for event in self.events]))
        for i in range(len(self.stops)) : associatedVisits.append(set(neighboorsServerAll.radius_neighbors(self.stops[i].position)[1][0]))
        #----------------------------------------------------------------------------------------------------#

        #---- Step 2 : Merge stop points onto poi and merge there visits ------------------------------------#
        aggregatedPOI=np.array([-1]*len(self.stops))
        numberOfPOI=0
        for i in range(len(self.stops)) :
            inIntersection=[]
            for j in range(len(self.stops)) :
                if (associatedVisits[i] & associatedVisits[j]) : inIntersection.append(j)
            poiId=min(aggregatedPOI[inIntersection])
            if (poiId==-1) :
                numberOfPOI+=1
                poiId=numberOfPOI
            aggregatedPOI[inIntersection]=poiId
        listPoiandNeighboorsIndex=[]
        for poiId in set(aggregatedPOI) :
            members=self.stops[aggregatedPOI==poiId]
            indices=np.array(range(len(self.stops)))[aggregatedPOI==poiId]
            neighboors=set()
            for i in indices : neighboors|=associatedVisits[i]
            poi=Poi(poiId,sum([p.longitude() for p in members])/len(members),sum([p.latitude() for p in members])/len(members))
            listPoiandNeighboorsIndex.append((poi,sorted(neighboors)))
        #----------------------------------------------------------------------------------------------------#

        #---- Step 3 : Creating the list of Poi -------------------------------------------------------------#
        infrequentVisits=[]
        for item in listPoiandNeighboorsIndex :
            poi,neighborsIndex=item
            j=neighborsIndex[0]
            for i in range(1,len(neighborsIndex)) :
                if (neighborsIndex[i] > neighborsIndex[i-1]+1) :
                    visit=Visit(-1,self.events[j].time,self.events[neighborsIndex[i-1]+1].time)
                    j=neighborsIndex[i]
                    if (visit.duration()>=self.stayTimeThres) : poi.addVisit(visit)
            k=neighborsIndex[-1]+1 if (neighborsIndex[-1]+1<len(self.events))else neighborsIndex[-1]
            visit=Visit(-1,self.events[j].time,self.events[k].time)
            if (visit.duration()>=self.stayTimeThres) :  poi.addVisit(visit)

            if (poi.visits) :
                if (len(poi.visits)>=self.freqThres) : self.poi.append(poi)
                else : infrequentVisits.extend(poi.visits)

        if (infrequentVisits) : self.poi.append(Poi('I',float('nan'),float('nan'),sorted(infrequentVisits,key = lambda visit : visit.arrival)))
        #----------------------------------------------------------------------------------------------------#
        self.finalize(self.poi,mergeVisits=False)
        return self.poi

