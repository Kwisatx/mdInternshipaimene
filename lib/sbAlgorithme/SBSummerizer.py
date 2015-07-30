import os
from main.SBPoiExtractor import SBPoiExtractor
from main.MobilityTraceReader import MobilityTraceReader
from datetime import datetime
import time

def summerize(path,distThres=0.0005,visitMinTime=600,freqThres=2) : 

    destinationDirectory="Resultats/Summary-"+os.path.splitext(os.path.basename(path))[0]
    if not os.path.exists(destinationDirectory) : os.mkdir(destinationDirectory)

    n=40
    
    print "-"*n
    print "File :",path
    print "Parameters :"
    print "Distance threshold :",distThres,"m"
    print "minimum visit time :",visitMinTime,"s"
    print "frequence threshold :",freqThres,"visits"
    print "-"*n
    
    print "Phase 1 - Preprocessing ..."
    start_time = time.time()
    reader=MobilityTraceReader(path)
    reader.readWithStop()
    reader.plotEvents()
    #reader.plotBearings()

    sBPoiExtractor=SBPoiExtractor(reader.events,reader.stops,distanceThres=distThres,stayTimeThres=visitMinTime,freqThres=freqThres)
    
    elapsed_time = time.time() - start_time
    print "Number of events :",len(sBPoiExtractor.events)
    print "Elapsed time :",elapsed_time,"s"
    print "-"*n

    print "Phase 2 Extracting POI ..."
    start_time = time.time()
    sBPoiExtractor.getPoi()
    elapsed_time = time.time() - start_time
    print "Elapsed time :",elapsed_time,"s"
    print "-"*n
    
    
    print "Phase 3 - Mobility Markov Model ..."
    start_time = time.time()
    sBPoiExtractor.drawMarkovMobilityModel(name=destinationDirectory+"/MarkovMobilityChain")
    elapsed_time = time.time() - start_time
    print "Elapsed time :",elapsed_time,"s"
    print "-"*n

    print "Phase 4 - Global Mobility Model ..."
    start_time = time.time()
    sBPoiExtractor.drawGlobalMobilityModel(name=destinationDirectory+"/Model")
    elapsed_time = time.time() - start_time
    print "Elapsed time :",elapsed_time,"s"
    print "-"*n
    
    print "Writing POI csv file ..."
    sBPoiExtractor.writePoi(outputFile=destinationDirectory+"/POI.csv")
    print "-"*n

    print "Writing visits csv file ..."
    sBPoiExtractor.writeVisits(outputFile=destinationDirectory+"/Visites.csv")
    print "-"*n

    print "Writing trajectories csv file ..."
    sBPoiExtractor.writeTrajectories(outputFile=destinationDirectory+"/Trajectories.csv")
    print "-"*n

    print "Plotting POI ..."
    sBPoiExtractor.plot(outputFile=destinationDirectory+"/POI.png",show=True,afficherText=True)
    print "-"*n
    
    
    
summerize("JSON/9.json")
