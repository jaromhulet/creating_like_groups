import nbr_hood as nbr
import random
import pandas as pd
import numpy as np
from math import exp


#create class for hill climb algorithms
class simulatedAnnealing(nbr.nbrHood):
    
    def __init__(self,df,numGroups,nbrhoodsize):
        
        super().__init__(df,numGroups)
        self.nbrhoodsize = nbrhoodsize
    
    def runSimulatedAnnealing(self,restarts,coolingSchedule,tempIters,aggMethod,distMetric,randStart='Y',startMetric=1):
        
        #random.seed(seed)
        obs = 0
    
        #create a starting solution
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)        
        
        globalBestNbr = startSolution
        globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
        
        currentSolution = startSolution
        
        
        #loop through restart
        for f in range(0,restarts):
            
            for temperature in coolingSchedule:
                
                for iters in range(0,tempIters):
                
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        
                        obs = obs + 1
                        
                        #calculate difference between current nbr and the best nbr
                        delta = self.totalDist(self.groupMetrics(i,aggMethod),distMetric) - self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                        
                        #calculate acceptance probability
                        acceptProb = exp(delta/temperature)
                        
                        #decide if it will be accepted 
                        if acceptProb > random.uniform(0,1):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                            #add break to make it first accept
                            break
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    
                    
            obs_statement = ("%s Solutions Examined" % obs)
            print("done")              
            
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist,obs_statement]                  