#create class for hill climb algorithms
class hillClimb(nbrHood):
    
    def __init__(self,df,numGroups):
        
        super().__init__(df,numGroups)
        
    
    def runHillClimb(self,selectMethod,restarts,startMetric=1,randStart='Y',seed=1920,randWalkProb=0.1):
        #start random seed
        random.seed(seed)
        
        #create a starting solution
        startSolution = self.df.startSol(randStart=randStart,startMetric=startMetric)
        
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
            
            for h in range(0,self.restarts):
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
                            #early exit as soon as a better solution is found
                            break

                    if currentSolution == bestNbr:
                        done = True
                    else:
                        currentSolution = bestNbr
        
        elif selectMethod == 'Random Walk':
            
            for h in range(0,self.restarts):
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

                    #implement random walk logic
                    if random.uniform(0,1) <= self.randWalkProb:                            
                        #pick a random nbr
                        currentSolution = Nbrhood[random.randint(0,len(Nbrhood))]
                                            
                    if currentSolution == bestNbr:
                        done = True
                    else:
                        currentSolution = bestNbr                            
            
    
        #return solution metric and solution
        return [self.groupMetrics(bestNbr),bestNbr]