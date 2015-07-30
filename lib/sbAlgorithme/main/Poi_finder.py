import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
#from mpl_toolkits.mplot3d import Axes3D
#from graphviz import Digraph

from Utils.Position import Position
from Utils.Poi import Poi
from Utils.Visit import Visit
from Utils.Trajectory import Trajectory

from math import isnan

class Poi_finder :
    def __init__(self,events) :
        self.events=events
        self.poi=[]
        self.visits=[]
        self.trajectories=[]

    def finalize(self,poi,mergeVisits=False) :
        """
        every class that inherit from this class should call finalize methode at the end of getPoi() which is mandatory 
        """

        self.poi=sorted(poi,key=lambda p : - p.accumulatedStayTime)
        i=1
        for p in self.poi :
            if (p.id != 'I') : 
                p.updateId(i)
                i+=1
            else : p.updateId('I')
        
        self.visits=[]
        for p in self.poi : self.visits.extend(p.visits)
        self.visits=sorted(self.visits,key=lambda visit : visit.arrival)

        if (mergeVisits) :   
            notMergedVisits=self.visits
            self.visits=[]
            i=0
            j=0
            while i<len(notMergedVisits) :
                if (i==len(notMergedVisits)-1 or notMergedVisits[i+1].poiId!=notMergedVisits[i].poiId) :
                    visit=notMergedVisits[i]
                    visit.arrival=notMergedVisits[j].arrival
                    self.visits.append(visit)
                    j=i+1
                i+=1
            for p in self.poi : p.setVisits([visit for visit in self.visits if visit.poiId==p.id])

        self.trajectories=[]
        for i in range(len(self.visits)-1) : self.trajectories.append(Trajectory(self.visits[i],self.visits[i+1]))

    #---------------- Mobility Markov Model -------------------------------------------------------------#
    def getMarkovMobilityModel(self) :
        transitionMatrix={}
        nombreDeSortant={}
        for t in self.trajectories :
            key=t.classe
            if (not nombreDeSortant.has_key(key[0])) : nombreDeSortant[key[0]]=1
            else : nombreDeSortant[key[0]]+=1
            if (not transitionMatrix.has_key(key)) : transitionMatrix[key]=1
            else : transitionMatrix[key]+=1
        for key in transitionMatrix.keys() : transitionMatrix[key]=float(transitionMatrix[key])/nombreDeSortant[key[0]]
        return transitionMatrix

    def drawMarkovMobilityModel(self,name="MobilityMarkovChain.png") :
        matrice=self.getMarkovMobilityModel()
        dot = Digraph()
        for poi in self.poi : dot.node(str(poi.id),str(poi.id)+"\n"+"Number of visit : "+str(len(poi.visits))+"\n"+"Time in : "+str(round(poi.accumulatedStayTime/3600,2))+" h")
        for key in matrice.keys() : dot.edge(str(key[0]), str(key[1]), label=str(matrice[key]))
        dot.format = 'pdf'
        dot.render(name, view=False)
    #----------------------------------------------------------------------------------------------------#

    #---------------- Global Mobility Model--------------------------------------------------------------#
    def getGlobalMobilityModel(self) :
        transitionMatrix={}
        for t in self.trajectories :
            key=t.classe
            if (not transitionMatrix.has_key(key)) : transitionMatrix[key]={}
            try : transitionMatrix[key][t.weekday]+=1
            except KeyError : transitionMatrix[key][t.weekday]=1
        return transitionMatrix
    
    def drawGlobalMobilityModel(self,name="model") :
        matrice=self.getGlobalMobilityModel()
        dot = Digraph()
        for poi in self.poi : dot.node(str(poi.id),str(poi.id)+"\n"+"Number of visit : "+str(len(poi.visits))+"\n"+"Time in : "+str(round(poi.accumulatedStayTime/3600,2))+" h")
        for key in matrice.keys() :
            label=""
            for k in matrice[key] : label+=k+" : "+str(matrice[key][k])+"\n"
            dot.edge(str(key[0]), str(key[1]), label=label)
        dot.format = 'pdf'
        dot.render(name, view=False)
    #----------------------------------------------------------------------------------------------------#
    
    #---------------- output In CSV ---------------------------------------------------------------------#
    def writePoi(self,outputFile) :
        csvFile=open(outputFile, 'w')
        HEADER="poi_id"+";"+"longitude"+";"+"latitude"+";"+"accumulatedStayTime"+";"+"NumberOfVisits"+"\n"
        csvFile.write(HEADER)
        for poi in self.poi :
            line="{0};{1};{2};{3};{4}\n".format(poi.id,poi.longitude(),poi.latitude(),poi.accumulatedStayTime,len(poi.visits))
            csvFile.write(line)
        csvFile.close();

    def writeVisits(self,outputFile,merge=False) :
        csvFile=open(outputFile, 'w')
        HEADER="Poi_id"+";"+"arrivee"+";"+"depart"+";"+"Duree"+";"+"\n"
        csvFile.write(HEADER)
        for visit in self.visits :
            line="{0};{1};{2};{3}\n".format(visit.poiId,visit.arrival,visit.departure,visit.duration())
            csvFile.write(line)
        csvFile.close();

    def writeTrajectories(self,outputFile) :
        csvFile=open(outputFile, 'w')
        HEADER="date"+";"+"time"+";"+"weekday"+";"+"daytype"+";"+"daypart"+";"+"classe"+"\n"
        csvFile.write(HEADER)
        for trajectory in self.trajectories :
            line=str(trajectory)+"\n"
            csvFile.write(line)
        csvFile.close();
    #--------------------------------------------------------------------------------------------

    #----------------Plot -----------------------------------------------------------------------
    def figurePoi(self,afficherText=False) :
        plt.figure(1)
        plt.clf()
        colors = cycle('bgrcmybgrcmybgrcmybgrcmy')
        pointLong=[e.longitude() for e in self.events]
        pointLat=[e.latitude() for e in self.events]
        img=plt.figure()
        plt.plot(pointLong,pointLat, 'o', markerfacecolor='k',markeredgecolor='k', markersize=1)
        for point, col in zip(self.poi, colors):
            if (not isnan(point.longitude())) : 
                plt.plot(point.longitude(),point.latitude(), 'o', markerfacecolor=col,markeredgecolor='k', markersize=15)
                if (afficherText) : plt.text(point.longitude(),point.latitude(),  str(point), bbox=dict(facecolor=col, alpha=0.5))
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title('Number of POI : %d' % len(self.poi))
        return img

    def figureAgenda(self) :
        plt.figure(1)
        plt.clf()
        img=plt.figure()
        colors = cycle('bgrcmybgrcmybgrcmybgrcmy')
        for poi, col in zip(self.poi, colors):
            for visit in poi.visits : plt.plot([visit.arrival, visit.departure], [2, 2], col+'-', lw=4)
        plt.xlabel("Time")
        plt.title('Number of POI : %d' % len(self.poi))
        return img
    #--------------------------------------------------------------------------------------------
