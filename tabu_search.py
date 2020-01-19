import nbr_hood as nbr
import random
import pandas as pd
import numpy as np


class tabuSearch(nbr.nbrHood):
    
    def __init__(self,df,numGroups,nbrhoodsize):
        
        super().__init__(df,numGroups)
        self.nbrhoodsize = nbrhoodsize
        
        
    def tabu(self,iters,tenure,startMetric=1,randStart='Y',aggMethod='avg',distMetric='euc'):
        
        #create simple function to get the difference in lists
        def listDiff(a, b): 
            return (list(set(a) - set(b)))           
        
        #create a starting solution
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)  
        
        globalBestNbr = startSolution
        globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)        
        
        
        obs = 0
        
        for h in range(0,iters):
    
            currentSolution = startSolution
            
            tabu_memory = []
    
            done = 0   
            
            while done == 0:
                
               
                    
                bestNbr = currentSolution
                bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                
                #manage tabu search memory. For double swaps, some things will get deleted with the same tenure. 
                for i in tabu_memory:
                    while len(tabu_memory) > tenure:
                        #delete first element
                        i.pop(0)
                
                #remove tabu elements before creating nbrs (this prevents them from being swapped)
                pos = -1
                for j in tabu_memory:
                    pos= pos + 1
                    for k in j:
                        bestNbr[pos].remove(k)
                        
                        
                #create nbrhood to iterate through (iterate through the nbrs of the nbrhood)  
                for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                    obs = obs + 1
                    
                    #re-add tabu before distance measurements
                    
                    #re-add tabu to bestNbr
                    pos = -1
                    for j in tabu_memory:
                        pos = pos + 1
                        for k in j:
                            bestNbr[pos].append(k)
                            
                    
                    
                    #re-add tabu to current neighbor being evaluated
                    pos = -1
                    for j in tabu_memory:
                        pos = pos + 1
                        for k in j:
                            i[pos].append(k)
                            
                    
                    if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                        bestNbr = i
                        bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                        print(bestDist)
                            
                if currentSolution == bestNbr:
                    done = 1
                else:
                    #find difference between currentSolution and bestNbr. Add that to end of tabu list
                    for i in tabu_memory:
                        i.append(listDiff(bestNbr[i],currentSolution[i]))
                                                       
                    currentSolution = bestNbr
                    
                    print("restart")
                    
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)                    
                    
                obs_statement = ("%s Solutions Examined" % obs)          
                
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist,obs_statement]            
                
        
        
        
        