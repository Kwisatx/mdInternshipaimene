from sbAlgorithme.main.MobilityTraceReader import MobilityTraceReader
from sbAlgorithme.main.SBPoiExtractor import SBPoiExtractor
import time

def getPoi(linesTraces,distThres=0.0005,visitMinTime=600,freqThres=2) :
    
    start_time = time.time()
    reader=MobilityTraceReader(linesTraces)
    reader.readWithStop()
    sBPoiExtractor=SBPoiExtractor(reader.events,reader.stops,distanceThres=distThres,stayTimeThres=visitMinTime,freqThres=freqThres)
    sBPoiExtractor.getPoi()
    poi=sBPoiExtractor.poi
	S="-"*60+"<br>"
    S+="POI"+"<br>"
    S+="-"*60+"<br>"
    for p in poi : S+=str(p)+"<br>"
    elapsed_time = time.time() - start_time
    S+="-"*60+"<br>"
    S+="Elapsed Time : "+str(elapsed_time)+" s"+"<br>"
    S+="-"*60
    return S
    
