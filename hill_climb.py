import nbr_hood as nbr
import random
import pandas as pd
import numpy as np

#create class for hill climb algorithms
class hillClimb(nbr.nbrHood):
    
    def __init__(self,df,numGroups):
        
        super().__init__(df,numGroups)
        
    
    def runHillClimb(self,selectMethod,restarts,aggMethod,distMetric,startMetric=1,randStart='Y',seed=1920,randWalkProb=0.1):
        #start random seed
        
        #random.seed(seed)
        
        #create a starting solution
        startSolution = self.startSol(randStart=randStart,startMetric=startMetric)
        
        #conditionally execute hill climb with best accept
        if selectMethod == 'BEST ACCEPT':
        
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
        

        
        #implement first accept method
        elif selectMethod == 'HILL CLIMB':
            
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
                    
        
        
        elif selectMethod == 'FIRST ACCEPT':
            
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
                            #add break to make it first accept
                            break
                            
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
            
        #conditionally execute random walk with best accept
        
        #I haven't actually coded the random walk yet.  Below is just Best Accept.
        #make necessary changes to make below code random walk.
        if selectMethod == 'RANDOM WALK':
            
            #create method to find random walked solution
            def rand_find(prob_list,rand_num):
                
                pos = -1
                
                for i in prob_list:
                    pos = pos + 1
                    if i > rand_num:
                        return pos            
        
            globalBestNbr = startSolution
            globalBestDist = self.totalDist(self.groupMetrics(startSolution,aggMethod),distMetric)
            
            for j in range(0,restarts):
                
            
                currentSolution = startSolution
            
                done = 0
            
                while done == 0:
                    
                    temp_nbr_df = pd.DataFrame(columns=['nbr','dist'])
                    bestNbr = currentSolution
                    bestDist = self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric)
                    
                    #make a list of nbr distances
                    for i in self.createNbrhood(currentSolution,self.numGroups):
                        
                        temp_nbr_df = temp_nbr_df.append({'nbr':i,'dist':self.totalDist(self.groupMetrics(i,aggMethod),distMetric)},ignore_index=True)
                    
                    #if none of the new neighbors are better than current solution, stop
                    dists = temp_nbr_df['dist']
                    if min(dists) > bestDist:
                        done = 1
                        break
                
                    temp_nbr_df = temp_nbr_df.sort_values(by='dist')
                    
                    temp_array = temp_nbr_df['dist'].values
                    
                    #flip array so lowest values have highest probability of selection
                    temp_array = np.flip(temp_array)
                    
                    temp_array_sum = np.sum(temp_array)
                    
                    temp_array = temp_array/temp_array_sum
                    
                    #create cumulative array to go into rand_find function
                    temp_array_cum = np.cumsum(temp_array)
                    
                    #find index of randomly selected nbr
                    index_num = rand_find(temp_array_cum,random.uniform(0,1))
                    
                    
                    bestNbr = temp_nbr_df['nbr'][index_num]
                    
                    
                      
                    currentSolution = bestNbr 
                    
                    print(self.totalDist(self.groupMetrics(currentSolution,aggMethod),distMetric))
                        
                        
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