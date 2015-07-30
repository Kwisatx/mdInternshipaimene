from cemmm.main.CEMMM import CEMMM
from sbAlgorithme.main.MobilityTraceReader import MobilityTraceReader
from sbAlgorithme.main.SBPoiExtractor import SBPoiExtractor
import time

def mine(linesTraces,distThres=0.0005,visitMinTime=600,freqThres=2) :
    
    start_time = time.time()
    reader=MobilityTraceReader(linesTraces)
    reader.readWithStop()
    sBPoiExtractor=SBPoiExtractor(reader.events,reader.stops,distanceThres=distThres,stayTimeThres=visitMinTime,freqThres=freqThres)
    sBPoiExtractor.getPoi()
    
    EM=CEMMM(sBPoiExtractor.poi,sBPoiExtractor.visits,sBPoiExtractor.trajectories)

    resultat = EM.cemmm(minimumSupport=3,k=10,maxSimilarite=0.2)
    #resultat = EM.cemmm_skylines(minimumSupport=3,relaxation=0.1)
    S="-"*60+"<br>"
    S+="Closed Exceptional Pattern"+"<br>"
    S+="-"*60+"<br>"
    for result in resultat : S+=str(result[0])+":"+str(result[1])+"<br>"
    elapsed_time = time.time() - start_time
    S+="-"*60+"<br>"
    S+="Elapsed Time : "+str(elapsed_time)+" s"+"<br>"
    S+="-"*60
    return S
    
