import math
from datetime import datetime,time
from Utils.Description import Description
#-------------------Pareto Optimums--------------------------------------------------------
def getParetoOptimums(result) :
    paretoOptimums=[]
    for r in result :
        rIsOptimum=True
        i=0
        while i<len(paretoOptimums) :
            p=paretoOptimums[i]
            rDominateP,pDominateR=(p[1]!=r[1]),True
            for ep,er in zip(p[1],r[1]) :
                rDominateP=rDominateP and (er>=ep)
                pDominateR=pDominateR and (ep>=er)
                if (not rDominateP and not pDominateR) : break
            if (rDominateP) : paretoOptimums.pop(i)
            elif (pDominateR) :rIsOptimum=False; break
            else : i+=1
        if (rIsOptimum) : paretoOptimums.append(r)
    return sorted(paretoOptimums,key = lambda element : -element[1][0])

def getParetoOptimumsWithRelaxation(result,relaxation) :
    paretoOptimums=[]
    for r in result :
        rIsOptimum=True
        i=0
        while i<len(paretoOptimums) :
            p=paretoOptimums[i]
            rDominateP,pDominateR=True,True
            for ep,er in zip(p[1],r[1]) :
                rDominateP=rDominateP and ((1-relaxation)*er>ep)
                pDominateR=pDominateR and ((1-relaxation)*ep>er)
                if (not rDominateP and not pDominateR) : break
            if (rDominateP) : paretoOptimums.pop(i)
            elif (pDominateR) :rIsOptimum=False; break
            else : i+=1
        if (rIsOptimum) : paretoOptimums.append(r)
    return sorted(paretoOptimums,key = lambda element : -element[1][0])
#--------------------------------------------------------------------------------------------
class CEMMM :
    def __init__(self,poi,visits,trajecories,precision=1) :
        self.poi=poi
        self.visits=visits
        self.trajectories=trajecories
        for t in self.trajectories :
            value=t.time.second+60*t.time.minute+3600*t.time.hour
            discret=(int(value)/precision)*precision
            t.time=time(discret/3600,(discret%3600)/60,discret%60)
        self.distributionGlobal=self.computeGlobalDistribution()
    #-----------------------------------------------------------------------------------------
    def computeGlobalDistribution(self) :
        distributionGlobal={}
        for t in self.trajectories :
            if (not distributionGlobal.has_key(t.classe)) : distributionGlobal[t.classe]=0
            distributionGlobal[t.classe]+=1
        for key in  distributionGlobal :
            distributionGlobal[key]/=float(len(self.trajectories))
        return distributionGlobal 
    #------------------------------------------------------------------------------------------
    def computeSupportObject(self,description) :
        indexes=[]
        for i in range(len(self.trajectories)) :
            if (description.isTrajectoryIn(self.trajectories[i])) : indexes.append(i)
        return indexes
    #--------------------Rudundency filter-----------------------------------------------------
    def getKNotRedundantMaximums(self,result,k,maxSimilarite) :
        maximums=[]
        numberOfResult=k
        while (len(result)>0 and numberOfResult>0) :
            items=zip(range(len(result)),result)
            maximum=max(items,key=lambda item : item[1][1][0])
            maximums.append(maximum[1])
            result.pop(maximum[0])
            maximumsIndexes=set(self.computeSupportObject(maximum[1][0]))
            i=0
            while i <len(result) :
                motif=result[i]
                motifIndexes=set(self.computeSupportObject(motif[0]))
                similarity=(1.*len(maximumsIndexes & motifIndexes))/len(maximumsIndexes | motifIndexes)
                if (similarity>maxSimilarite) : result.pop(i)
                else : i+=1
            numberOfResult-=1
        return maximums
    #--------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------
    def computeClosed(self,description) :
        distributionGlobal=self.distributionGlobal
        distributionLocal={}
        closedDescription=Description([],[description.timeIntervalRestriction[1],description.timeIntervalRestriction[0]])
        #----------------------------------------------------------------------------------------
        support=0
        for t in self.trajectories :
            if (description.isTrajectoryIn(t)) :
                closedDescription&=t
                support+=1
                if (not distributionLocal.has_key(t.classe)) : distributionLocal[t.classe]=1
                else : distributionLocal[t.classe]+=1
        #----------------------------------------------------------------------------------------
        difference=0
        for key in distributionGlobal :
            if (not distributionLocal.has_key(key)) :d=-distributionGlobal[key]
            else :
                distributionLocal[key]/=float(support)
                d=(distributionLocal[key]-distributionGlobal[key])
                difference+=float(abs(d))/(1-abs(d))
        #---------------------------------------------------------------------------------------
        alpha=0
        freq=(float(support)/len(self.trajectories))
        quality=(freq**alpha)*round(difference,2)
        return support,[quality,support],closedDescription
    #--------------------------------------------------------------------------------------------
    def mineClosedDescriptions(self,description,attributActuel,p,sortedHours,hoursValueIndexMap,closedDescriptions,minimumSupport) :
        support,measures,closedDescription=self.computeClosed(description)
        if (support<minimumSupport or description.compareCannonicOrder(closedDescription,attributActuel)==False) : return
        closedDescriptions.append([closedDescription,measures])
        if (attributActuel==0) :
            if (not (len(closedDescription.weekdayRestriction)==1 or p==len(closedDescription.weekdayRestriction))) :
                while p<len(closedDescription.weekdayRestriction) :
                    newDescription=closedDescription.restrictWeekdays(p)
                    self.mineClosedDescriptions(newDescription,0,p,sortedHours,hoursValueIndexMap,closedDescriptions,minimumSupport)
                    p+=1
            p=0
        if (closedDescription.duration()>0) :
            if (p==0) :
                newDescritpion=closedDescription.restrictRightTimeInterval(sortedHours,hoursValueIndexMap)
                self.mineClosedDescriptions(newDescritpion,1,0,sortedHours,hoursValueIndexMap,closedDescriptions,minimumSupport)
            newDescritpion=closedDescription.restrictLeftTimeInterval(sortedHours,hoursValueIndexMap)
            self.mineClosedDescriptions(newDescritpion,1,1,sortedHours,hoursValueIndexMap,closedDescriptions,minimumSupport)
    #-----------------------------------------------------------------------------------------------
    def cemmm(self,minimumSupport,k,maxSimilarite) :
        #--------------------------------------------------------------------------------------------
        values=set()
        times=[]
        for t in self.trajectories : values.add(int(t.time.second+60*t.time.minute+3600*t.time.hour))
        for v in values : times.append(time(v/3600,(v%3600)/60,v%60))
        sortedHours=sorted(times)
        hoursValueIndexMap={}
        for i in range(len(sortedHours)) : hoursValueIndexMap[str(sortedHours[i])]=i
        weekdaysValues=sorted(set([t.weekday for t in self.trajectories]))
        #--------------------------------------------------------------------------------------------
        description=Description(weekdaysValues,[sortedHours[0],sortedHours[-1]])
        result=[]
        self.mineClosedDescriptions(description,0,0,sortedHours,hoursValueIndexMap,result,minimumSupport=minimumSupport)
        #--------------------------------------------------------------------------------------------
        return self.getKNotRedundantMaximums(result,k,maxSimilarite)
    #-----------------------------------------------------------------------------------------------
    def cemmm_skylines(self,minimumSupport,relaxation=0) :
        #--------------------------------------------------------------------------------------------
        values=set()
        times=[]
        for t in self.trajectories : values.add(int(t.time.second+60*t.time.minute+3600*t.time.hour))
        for v in values : times.append(time(v/3600,(v%3600)/60,v%60))
        sortedHours=sorted(times)
        hoursValueIndexMap={}
        for i in range(len(sortedHours)) : hoursValueIndexMap[str(sortedHours[i])]=i
        weekdaysValues=sorted(set([t.weekday for t in self.trajectories]))
        #--------------------------------------------------------------------------------------------
        description=Description(weekdaysValues,[sortedHours[0],sortedHours[-1]])
        result=[]
        self.mineClosedDescriptions(description,0,0,sortedHours,hoursValueIndexMap,result,minimumSupport=minimumSupport)
        #--------------------------------------------------------------------------------------------
        if (relaxation==0) : return getParetoOptimums(result) 
        return getParetoOptimumsWithRelaxation(result,relaxation)
