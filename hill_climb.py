import nbr_hood as nbr
import random
import pandas as pd

#create class for hill climb algorithms
class hillClimb(nbr.nbrHood):
    
    def __init__(self,df,numGroups):
        
        super().__init__(df,numGroups)
        
    
    def runHillClimb(self,selectMethod,restarts,aggMethod,distMetric,startMetric=1,randStart='Y',seed=1920,randWalkProb=0.1):
        #start random seed
        
        #random.seed(seed)
        
        #create a starting solution
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)
        
        #conditionally execute hill climb with best select
        if selectMethod == 'Best Select':
            for h in range(0,restarts):
            
                currentSolution = startSolution

                done = False

                while done == False:
                    bestNbr = currentSolution

                    #create neighborhood
                    Nbrhood = createNbrhood(currentSolution)

                    #loop thru all nbrs to get distance value
                    for i in range(0,len(Nbrhood)):
                        if self.groupMetrics(Nbrhood[i]) < self.groupMetrics(bestNbr):
                            bestNbr = Nbrhood[i]

                    if currentSolution == bestNbr:
                        done = True
                    else:
                        currentSolution = bestNbr
        
        #implement first accept method
        elif selectMethod == 'First Accept':
            
            for h in range(0,restarts):
                currentSolution = startSolution

                done = False

                while done == False:
                    bestNbr = currentSolution
                    #bestDist = self.totalDist(currentSolution,distMetric)

                    #create neighborhood
                    Nbrhood = self.createNbrhood(currentSolution,self.numGroups)

                    #loop thru all nbrs to get distance value
                    for i in range(0,len(Nbrhood)):
                        currentBest = self.groupMetrics(Nbrhood[i],aggMethod)
                        current = self.groupMetrics(bestNbr,aggMethod)
                        
                        if self.totalDist(currentBest,distMetric) < self.totalDist(current,distMetric):
                            bestNbr = Nbrhood[i]
                            bestDist = self.totalDist(currentBest,distMetric)
                            #early exit as soon as a better solution is found
                            break

                    if currentSolution == bestNbr:
                        done = True
                    else:
                        currentSolution = bestNbr
                    print("Iteration best solution distance = %s " % bestDist)
        
        elif selectMethod == 'Random Walk':
            
            for h in range(0,restarts):
                currentSolution = startSolution

                done = False

                while done == False:
                    bestNbr = currentSolution

                    #create neighborhood
                    Nbrhood = self.createNbrhood(currentSolution)

                    #loop thru all nbrs to get distance value
                    for i in range(0,len(Nbrhood)):
                        if self.groupMetrics(Nbrhood[i]) < self.groupMetrics(bestNbr):
                            bestNbr = Nbrhood[i]

                    #implement random walk logic
                    if random.uniform(0,1) <= self.randWalkProb:                            
                        #pick a random nbr
                        currentSolution = Nbrhood[random.randint(0,len(Nbrhood))]
                                            
                    if currentSolution == bestNbr:
                        done = True
                    else:
                        currentSolution = bestNbr                            
            
    
        #return solution metric and solution
        return [self.groupMetrics(bestNbr,aggMethod),bestNbr,bestDist]