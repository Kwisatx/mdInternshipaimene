import os
import time
import zipfile

from tracesAnalyser.MobilityTraceReader import MobilityTraceReader
from tracesAnalyser.PoiReader import PoiReader

from tracesAnalyser.SBPoiExtractor import SBPoiExtractor
from tracesAnalyser.WBPoiExtractor import WBPoiExtractor
from tracesAnalyser.CEMMM import CEMMM


STOPBASEDALGORITHME="SB"
WEIGHTBASEDALGORITHME="WB"


class Server :
    def __init__(self,linesTraces=None,method=STOPBASEDALGORITHME,linesPoi=None,linesVisits=None) :
        if (linesTraces) :
            self.method=method
            reader=MobilityTraceReader(linesTraces)
            if (method==STOPBASEDALGORITHME) :
                reader.readWithStop()
                self.events,self.stops=reader.events,reader.stops
            elif (method==WEIGHTBASEDALGORITHME) :
                reader.readWithPreProcessing(samplingTime=0,distanceMin=0,tempsMaxPerteSignal=float("inf"))
                self.events=reader.events
        elif (linesPoi and linesVisits) :
            poiReader=PoiReader(linesPoi,linesVisits)
            self.poi=poiReader.poi
            self.visits=poiReader.visits
            self.trajectories=poiReader.trajectories
    #-------------------------------------------------------------------------------------------------------------
    def getPoiVisitsAndTrajectories(self,distThres=0.0005,visitMinTime=600,freqThres=2) :
        if (self.method==STOPBASEDALGORITHME) : self.poiExtractor=SBPoiExtractor(self.events,self.stops,distanceThres=distThres,stayTimeThres=visitMinTime,freqThres=freqThres)
        elif (self.method==WEIGHTBASEDALGORITHME) : self.poiExtractor==WBPoiExtractor(self.events,step=0.0001,overlap=1,visitMinTime=300,bandwidth=0.001,weighter=VISITDURATION)
        self.poiExtractor.getPoi()
        self.poi=self.poiExtractor.poi
        self.visits=self.poiExtractor.visits
        self.trajectories=self.poiExtractor.trajectories
    #-------------------------------------------------------------------------------------------------------------
    KFIRST="K-FIRST"
    SKYPATTERN="SKY-PATTERN"
    def getCEMMM(self,minimumSupport=3,k=10,maxSimilarite=0.2,relaxation=0.1,method=KFIRST) :
        closedPatternExtractor=CEMMM(self.poi,self.visits,self.trajectories)
        if (method==KFIRST) : self.cemmm=closedPatternExtractor.cemmm(minimumSupport=minimumSupport,k=k,maxSimilarite=maxSimilarite)
        elif (method==SKYPATTERN) : self.cemmm=closedPatternExtractor.cemmm_skylines(minimumSupport=minimumSupport,relaxation=relaxation)
    #-------------------------------------------------------------------------------------------------------------
    #                   Temporary Displays   
    #-------------------------------------------------------------------------------------------------------------
    def stringPOI(self) :
        S="-"*60+"<br>"
        S+="POI"+"<br>"
        S+="-"*60+"<br>"
        for p in self.poi : S+=str(p)+"<br>"
        S+="-"*60+"<br>"
        return S
    #-------------------------------------------------------------------------------------------------------------
    def stringVisits(self) :
        S="-"*60+"<br>"
        S+="Visits"+"<br>"
        S+="-"*60+"<br>"
        for v in self.visits : S+=str(v)+"<br>"
        S+="-"*60+"<br>"
        return S
    #-------------------------------------------------------------------------------------------------------------
    def stringTrajectories(self) :
        S="-"*60+"<br>"
        S+="Trajectories"+"<br>"
        S+="-"*60+"<br>"
        for t in self.trajectories : S+=str(t)+"<br>"
        S+="-"*60+"<br>"
        return S
    #-------------------------------------------------------------------------------------------------------------
    def createZipFilePoiVisitsTrajectories(self) :
        destinationDirectory="Resultats"
        if not os.path.exists(destinationDirectory) : os.mkdir(destinationDirectory)

        self.poiExtractor.writePoi("{0}/poi.csv".format(destinationDirectory))
        self.poiExtractor.writeVisits("{0}/visits.csv".format(destinationDirectory))
        self.poiExtractor.writeTrajectories("{0}/trajectories.csv".format(destinationDirectory))

        zipFilePath="{0}/info.zip".format(destinationDirectory)
        zf=zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)

        zf.write("{0}/poi.csv".format(destinationDirectory),"poi.csv")
        zf.write("{0}/visits.csv".format(destinationDirectory),"visits.csv")
        zf.write("{0}/trajectories.csv".format(destinationDirectory),"trajectories.csv")

        zf.close()
        return zipFilePath
    #-------------------------------------------------------------------------------------------------------------
    def stringCEMMM(self) :
        S="-"*60+"<br>"
        S+="Closed Exceptional Pattern"+"<br>"
        S+="-"*60+"<br>"
        for result in self.cemmm : S+=str(result[0])+":"+str(result[1])+"<br>"
        S+="-"*60+"<br>"
        return S
    #-------------------------------------------------------------------------------------------------------------
        
