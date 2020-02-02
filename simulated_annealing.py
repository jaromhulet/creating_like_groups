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
        
        currentSolution = startSolution
        currentDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
        for temperature in coolingSchedule:
                
            print('temparature is %s' % temperature)
                
            for iters in range(0,tempIters):
                              
                temp_nbr = self.createNbrhood(currentSolution,2)
                
                        
                obs = obs + 1
                       
                        
                #calculate difference between current nbr and the best nbr
                delta = self.totalDist(self.groupMetrics(temp_nbr[0],aggMethod),distMetric) - self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                #calculate acceptance probability
                if delta < 0:
                    acceptProb = 1.1
                else:
                    acceptProb = exp(-delta/temperature)
                        
                #decide if it will be accepted 
                if acceptProb > random.uniform(0,1):
                    currentSolution = temp_nbr[0]
                    currentDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    print(currentDist)
                    
                    
            obs_statement = ("%s Solutions Examined" % obs)
            print("done")              
            
        #return solution metric and solution
        return [self.groupMetrics(currentSolution,aggMethod),currentSolution,currentDist,obs_statement]                  