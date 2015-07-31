import math
from scipy import sparse
import numpy as np
from Utils.Poi import Poi
from Utils.Visit import Visit
from Poi_finder import Poi_finder
from sklearn.cluster import MeanShift
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

VISITDURATION="VISIT_DURATION"
SIGNALLOSS="SIGNAL_LOSS"

class WBPoiExtractor(Poi_finder) :
    def __init__(self,events,step=0.0001,overlap=1,visitMinTime=300,freqThres=1,bandwidth=0.001,weighter=VISITDURATION) :
        self.events=events
        self.step=step
        self.overlap=overlap
        self.visitMinTime=visitMinTime
        self.freqThres=freqThres
        self.bandwidth=bandwidth
        
        longitudes = [e.longitude() for e in self.events] 
        latitudes = [e.latitude() for e in self.events]
        self.minLong=min(longitudes)
        self.minLat=min(latitudes)
        self.maxLong=max(longitudes)
        self.maxLat=max(latitudes)
        self.maxI=int((self.maxLong-self.minLong)/self.step)
        self.maxJ=int((self.maxLat-self.minLat)/self.step)
        #------------- event-to-cell impact mask --------------------------------
        maximum=2*self.overlap+1 
        self.poids={}
        for i in xrange(-self.overlap,self.overlap+1) :
            for j in xrange(-self.overlap,self.overlap+1) :
                poid=1-float(abs(i)+abs(j))/maximum
                self.poids[(i,j)]=poid
        #-------------------------------------------------------------
        if (weighter==SIGNALLOSS) : self.weightAll=self.weightWithSignalLoss
        else : self.weightAll=self.weightWithVisits 

    #---------------- Weighters -----------------------------------------------------------------------------#

    def toCell(self,event) :
        return (int((event.longitude()-self.minLong)/self.step),int((event.latitude()-self.minLat)/self.step))

    def toAffectedRegion(self,event) :
        return [int((event.longitude()-self.minLong)/self.step)-self.overlap,int((event.longitude()-self.minLong)/self.step)+self.overlap,
                int((event.latitude()-self.minLat)/self.step)-self.overlap,int((event.latitude()-self.minLat)/self.step)+self.overlap]
        
    def region(self,eventIndex) :
        event=self.events[eventIndex]
        poids=self.poids
        overlap=self.overlap
        weights=self.weights

        center=self.toCell(event)
        l=[]
        c=[]
        for i in range(center[0]-overlap,center[0]+overlap+1) :
            if (i<0 or i>self.maxI) : continue
            for j in range(center[1]-overlap,center[1]+overlap+1) :
                if (j<0 or j>self.maxJ or (not weights.has_key((i,j)) and 1<1)) : continue
                l.append((i,j))
                c.append(poids[(i-center[0],j-center[1])])
        return l,c
    
    def weightWithVisits(self) :
        self.weights={}
        weights=self.weights
        region=self.region
        visitMinTime=self.visitMinTime
        nextEvent=self.events[0]
        numberOfEvents=len(self.events)
        for k in range(numberOfEvents-1) :
            event=nextEvent
            nextEvent=self.events[k+1]
            affectedRegion=self.toAffectedRegion(nextEvent)
            neighboorhood,weightOfNeighboorhood=region(k)
            for key,weightOfKey in zip(neighboorhood,weightOfNeighboorhood) :
                if (not weights.has_key(key)) : weights[key]={"weight":0,"firstEventOfVisit":None,"massOfVisit":0,"numberOfEventsInActualVisit":0,"visits":[],"mass":0,"center":event}
                cell=weights[key]
                cell["center"]=(cell["center"]*cell["mass"]+event)/(cell["mass"]+1)
                cell["mass"]+=1
                if (not cell["firstEventOfVisit"]) : cell["firstEventOfVisit"]=event
                if (nextEvent.part==event.part) :
                    cell["massOfVisit"]+=weightOfKey
                    cell["numberOfEventsInActualVisit"]+=1
                isEndOfVisit=(nextEvent.part > event.part) or not (affectedRegion[0]<=key[0]<=affectedRegion[1] and affectedRegion[2]<=key[1]<=affectedRegion[3])
                if (isEndOfVisit) :
                    lastEventOfVisit=nextEvent if (nextEvent.part==event.part) else event
                    durationOfVisit=lastEventOfVisit.delai(cell["firstEventOfVisit"])
                    if (durationOfVisit>=visitMinTime) :
                        cell["weight"]+=(cell["massOfVisit"]/cell["numberOfEventsInActualVisit"])*durationOfVisit
                        cell["visits"].append(Visit(0,cell["firstEventOfVisit"].time,lastEventOfVisit.time))
                    cell["firstEventOfVisit"]=None
                    cell["massOfVisit"]=0
                    cell["numberOfEventsInActualVisit"]=0 
        return self.weights

    def weightWithSignalLoss(self) :
        self.weights={}
        weights=self.weights
        region=self.region
        visitMinTime=self.visitMinTime
        nextEvent=self.events[0]
        numberOfEvents=len(self.events)
        for k in range(numberOfEvents-1) :
            event=nextEvent
            nextEvent=self.events[k+1]
            key=(int((event.longitude()-self.minLong)/self.step),int((event.latitude()-self.minLat)/self.step))
            if (not weights.has_key(key)) : weights[key]={"weight":0,"visits":[],"mass":0,"center":event}
            cell=weights[key]
            cell["center"]=(cell["center"]*cell["mass"]+event)/(cell["mass"]+1)
            cell["mass"]+=1
            if (nextEvent.delai(event)>=visitMinTime) :
                cell["weight"]+=nextEvent.delai(event)
                cell["visits"].append(Visit(0,event.time,nextEvent.time))
        return self.weights

    #-------------------Poi and visit extraction ------------------------------------------------------------#

    def getPoi(self) :
        #---- Step 1 : Eliminate 0-weighted cell ------------------------------------------------------------#
        for key in self.weights.keys() :
            if (self.weights[key]["weight"]==0) : self.weights.pop(key, None)
        #----------------------------------------------------------------------------------------------------#
        
        keys=self.weights.keys()
        indexes=np.array(keys)
        positions=np.array([self.weights[key]["center"] for key in keys])
        weights=np.array([self.weights[key]["weight"] for key in keys])

        #---- Step 2 : Mode clustering of cells (meanshift) -------------------------------------------------#
        data=np.array([[position.longitude(),position.latitude()] for position in positions])
        ms = MeanShift(bandwidth=self.bandwidth,bin_seeding=True)
        ms.fit(data)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_
        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique) - (1 if -1 in labels else 0)
        #----------------------------------------------------------------------------------------------------#

        #---- Step 3 : Creating the list of Poi -------------------------------------------------------------#   
        self.poi=[]
        infrequentVisits=[]
        for k in range(n_clusters_) :
            #center = cluster_centers[k]
            my_members = labels == k
            weightedPositions=zip(list(indexes[my_members]),list(positions[my_members]),list(weights[my_members]))
            maximum=max(weightedPositions,key=lambda element : element[2])
            poi=Poi(k,maximum[1].longitude(),maximum[1].latitude())
            
            temporaryVisits=[]
            for element in weightedPositions :
                for visit in self.weights[tuple(element[0])]["visits"] :
                    temporaryVisits.append(visit)
            temporaryVisits=sorted(temporaryVisits,key=lambda visit : visit.arrival)

            visits=[temporaryVisits[0]]
            for i in range(1,len(temporaryVisits)) :
                lastVisit=visits[-1]
                visit=temporaryVisits[i]
                if (visit.arrival<=lastVisit.departure) :
                    lastVisit.departure=max(lastVisit.departure,visit.departure)
                else : visits.append(visit)

            if (len(visits)>=self.freqThres) :    
                poi.setVisits(visits)
                self.poi.append(poi)
            else : infrequentVisits.extend(visits)

        if (infrequentVisits) : self.poi.append(Poi('I',float('nan'),float('nan'),sorted(infrequentVisits,key = lambda visit : visit.arrival)))
        #----------------------------------------------------------------------------------------------------#

        self.finalize(self.poi,mergeVisits=False)
        return self.poi

    #--------------------Draw heatmap -----------------------------------------------------------------------#

    def heatmap(self,cadre=None) :
        """
        cadre = [minLongitude,maxLonngitude,minLatitude,maxLatitude]
        """
        weights=self.weights
        keys=weights.keys()
        size=10
        if (not cadre) : 
            longitudeMax=max(keys,key=lambda key : key[0])[0]+1
            latitudeMax=max(keys,key=lambda key : key[1])[1]+1
            M=sparse.dok_matrix((latitudeMax,longitudeMax))
            for key in keys : M[key[1],key[0]]=math.log(weights[key]["weight"]+1.2)
            DictMatrix=zip([key[0]*self.step+self.minLat for key in M.keys()],[key[1]*self.step+self.minLong for key in M.keys()],[M[key] for key in M.keys()])
        else :
            minLong=cadre[0]
            maxLong=cadre[1]
            minLat=cadre[2]
            maxLat=cadre[3]
            sizeLong=int(round(float(maxLong-minLong)/self.step))+1
            sizeLat=int(round(float(maxLat-minLat)/self.step))+1
            M=sparse.dok_matrix((sizeLat,sizeLong))
            for key in keys :
                longKey=key[0]*self.step+self.minLong
                latKey=key[1]*self.step+self.minLat
                if (minLat<latKey<maxLat and minLong<longKey<maxLong) :
                    key2=(int(round((latKey-minLat)/self.step)),int(round((longKey-minLong)/self.step)))
                    M[key2[0],key2[1]]=math.log(weights[key]["weight"]+1.2)
            DictMatrix=zip([key[0]*self.step+minLat for key in M.keys()],[key[1]*self.step+minLong for key in M.keys()],[M[key] for key in M.keys()]) 
        DictMatrix=np.array(sorted(DictMatrix,key = lambda element : element[2]))
        img=plt.figure()
        plt.subplot(111, axisbg='black')
        plt.scatter(DictMatrix[:,1], DictMatrix[:,0],s=size,c=DictMatrix[:,2], cmap=plt.cm.hot,marker='s',edgecolors='none')
        cb = plt.colorbar()
        cb.set_label('Weight in log scale')
        #if (img) : img.savefig(name,dpi = 500)
        return img

    #-----------------------------------------------------------------------------------------------------------#
