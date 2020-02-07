import nbr_hood as nbr
import random
import pandas as pd
import numpy as np

#create class for hill climb algorithms
class VNS(nbr.nbrHood):
    
    def __init__(self,df,numGroups,nbrhoodsize):
        
        super().__init__(df,numGroups)
        self.nbrhoodsize = nbrhoodsize
    
    
    #when a new global minimum is found, expand search to 2 swap, maybe even 3 swap?
    def runVNS(self,VNS_type,restarts,aggMethod,distMetric,startMetric=1,randStart='Y',expandFactor=2,nSwaps=2):
        
        #VNS_type has 3 options -- EXPAND, 2SWAP, 3SWAP. EXPAND increases nbrhood size by a specified factor when a minimum is found,
                                   #2SWAP changes nbrhood to 2 swap when min is found
                                   #3SWAP changes nbrhood to 3 swap when min is found
        
        obs = 0
        
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)
        
        #conditionally execute hill climb with EXPAND
        if VNS_type == 'EXPAND':
        
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                #do a random start if it is not the first iteration
                if j == 0:
                    currentSolution = startSolution
                else:
                    currentSolution = self.startSol(randStart=randStart,startMetric=startMetric)
            
                done = 0
            
                while done == 0:
                    
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                            
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                        
                        
                print("restart")
                
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    print("Start Expanded Search")
                    
                    best_nbr = 0
                
                    while best_nbr == 0:
                        
                        bestNbr = currentSolution
                        bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                        
                        for i in self.createNbrhood(currentSolution,int(round(self.nbrhoodsize*expandFactor,0))):
                            obs = obs + 1
                            if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                                bestNbr = i
                                bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                                
                                
                                
                        if currentSolution == bestNbr:
                            best_nbr = 1
                            globalBestNbr = bestNbr
                            print("Global Best = %s" % globalBestDist)                            
                        else:
                            currentSolution = bestNbr       
                    print("End expanded search")
                
                obs_statement = ("%s Solutions Examined" % obs)
                print("done")                       
                    
                    
            
        #conditionally execute hill climb with EXPAND
        elif VNS_type == 'NSWAP':
            
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
                
            for j in range(0,restarts):
                    
                
                #do a random start if it is not the first iteration
                if j == 0:
                    currentSolution = startSolution
                else:
                    currentSolution = self.startSol(randStart=randStart,startMetric=startMetric)
                
                done = 0
                
                while done == 0:
                        
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                        
                    for i in self.createNbrhood(currentSolution,self.nbrhoodsize):
                        obs = obs + 1
                        if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                            bestNbr = i
                            bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                            print(bestDist)
                                
                    if currentSolution == bestNbr:
                        done = 1
                    else:
                        currentSolution = bestNbr 
                            
                            
                print("restart")
                    
                if bestDist < globalBestDist:
                    globalBestNbr = bestNbr
                    globalBestDist = self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric)
                    print("New Global Best = %s" % globalBestDist)
                    print("Start %s Swap Search" % nSwaps)
                        
                    best_nbr = 0
                    
                    while best_nbr == 0:
                            
                        bestNbr = currentSolution
                        bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                            
                        for i in self.createNbrhood(currentSolution,self.nbrhoodsize,numSwaps=nSwaps):
                            obs = obs + 1
                            if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                                bestNbr = i
                                bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                                    
                                    
                                    
                        if currentSolution == bestNbr:
                            best_nbr = 1
                            globalBestNbr = bestNbr
                            print("Global Best = %s" % globalBestDist)                            
                        else:
                            currentSolution = bestNbr       
                    print("End expanded search")
                        
                        
                    
            obs_statement = ("%s Solutions Examined" % obs)
            print("done")              
            
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist,obs_statement]            
        
        
        
        
        
        
        
