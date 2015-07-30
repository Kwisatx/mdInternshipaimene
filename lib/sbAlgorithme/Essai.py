from main.MobilityTraceReader import MobilityTraceReader
from main.SBPoiExtractor import SBPoiExtractor

def essai(linesTraces,distThres=0.0005,visitMinTime=600,freqThres=2) : 
    reader=MobilityTraceReader(linesTraces)
    reader.readWithStop()
    sBPoiExtractor=SBPoiExtractor(reader.events,reader.stops,distanceThres=distThres,stayTimeThres=visitMinTime,freqThres=freqThres)
    sBPoiExtractor.getPoi()
    return sBPoiExtractor.figureAgenda()
