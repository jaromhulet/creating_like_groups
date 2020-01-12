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
               
            #my current solultion gets reset at each restart.  That's why I'm not getting the best from all restarts.  I'm only getting the best from the most 
            #recent restart.  I need to fix this by giving permanance to the best solution of all restarts
            for h in range(0,restarts):
                
                #new starting solution
                currentSolution = self.startSol(randStart=randStart,startMetric=startMetric)
                
                print("restart %s" % h)

                done = False

                while done == False:
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)

                    #create neighborhood
                    Nbrhood = self.createNbrhood(currentSolution,self.numGroups)

                    #loop thru all nbrs to get distance value
                    for i in range(0,len(Nbrhood)):
                        #current = self.groupMetrics(Nbrhood[i],aggMethod)
                        #currentBest = self.groupMetrics(bestNbr,aggMethod)
                        
                        if self.totalDist(self.groupMetrics(Nbrhood[i],aggMethod),distMetric) < self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric):
                            bestNbr = Nbrhood[i]
                            bestDist = self.totalDist(self.groupMetrics(Nbrhood[i],aggMethod),distMetric)
                            #early exit as soon as a better solution is found
                            break

                    if currentSolution == bestNbr:
                        #bestNbr = currentSolution
                        #bestDist = self.totalDist(self.groupMetrics(Nbrhood[i],aggMethod),distMetric)
                        done = True
                    else:
                        currentSolution = bestNbr
                    print("Iteration best solution distance = %s " % self.totalDist(self.groupMetrics(Nbrhood[i],aggMethod),distMetric))
        
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
                        
        elif selectMethod == 'TEST':
            
            currentSolution = startSolution
            
            done = 0
            
            while done == 0:
                
                bestNbr = currentSolution
                bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                
                for i in self.createNbrhood(currentSolution,self.numGroups):
                    if self.totalDist(self.groupMetrics(i,aggMethod),distMetric) < self.totalDist(self.groupMetrics(bestNbr,aggMethod),distMetric):
                        bestNbr = i
                        bestDist = self.totalDist(self.groupMetrics(i,aggMethod),distMetric)
                        print(bestDist)
                        
                if currentSolution == bestNbr:
                    done = 1
                else:
                    currentSolution = bestNbr
                    
        
        
        elif selectMethod == 'TEST2':
            
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    for i in self.createNbrhood(currentSolution,self.numGroups):
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
                    
                    
            #put the globals back into the locals so the return statement returns the global bests
            #bestNbr = globalBestNbr
            #bestDist = globalBestDist
            
            print("done")
                    
                
            
    
        #return solution metric and solution
        return [self.groupMetrics(globalBestNbr,aggMethod),globalBestNbr,globalBestDist]