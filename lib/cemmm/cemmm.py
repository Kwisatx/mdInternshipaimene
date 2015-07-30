from main.CEMMM import CEMMM
from main.PoiReader import PoiReader
import time

def cemmm(poiLines,visitsLines) :
    start_time = time.time()
    S="-"*60+"<br>"
    S+="Closed Exceptional Pattern"+"<br>"
    S+="-"*60+"<br>"
    reader=PoiReader(poiLines,visitsLines)
    EM=CEMMM(reader.poi,reader.visits,reader.trajectories)
    resultat = EM.cemmm(minimumSupport=3,k=10,maxSimilarite=0.2)
    #resultat = EM.cemmm_skylines(minimumSupport=3,relaxation=0.1)
    for result in resultat : S+=str(result[0])+":"+str(result[1])+"<br>"
    elapsed_time = time.time() - start_time
    S+="-"*60+"<br>"
    S+="Elapsed Time : "+str(elapsed_time)+" s"+"<br>"
    S+="-"*60
    return S
    
