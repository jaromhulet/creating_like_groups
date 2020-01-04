#Inherits baseHueristic class
#Provides random neighborhood start, and neighborhood creation based on current solution space
#Does not provide any kind of decisions based on neighborhoods => use specific heuristic classes for those methods
class nbrHood(baseHeuristic):
    #nbrHoodSize = the number of nbrs that will be explored
    #numGroups = the number of groups that the hueristic will put the elements into
    #numSwaps = how many swaps to get neighbors
    #startMetric = the column number of the dataframe that will be used to estimate a good starting point ==> defaults to 1
    #extraSwapProb = probability of switching 2 elements for one.  This allows the number of elements in the groups to migrate,
    #  If this is 0, the groups will have the same number of elements as the starting solution. This will confine the search
    #groupsSize = a list that has number of elements equal to numGroups. This forces each group to have a specified number 
    #  of elements
    #elemSum = limits the number of elements used in all three groups. If used only wants 20 elements to be used among 3
    #  groups, numGroups = 3, elemSum = 20. This does not constrain how many elements are in each group, use groupSize
    #  to control number elements in each group
    #seed = any arbitrary number used to get random numbers
    #randStart = User decide to use random start or deterministic start based on a specific column. Acceptable values are 'Y'
    #  and 'N'
    
    #I think I'm not going to do anything with groupSize or elemSum right now.  Maybe an add on for a future version
    
    def __init__(self,df,numGroups):
        
        super().__init__(df)
        #user defined attributes
        self.numGroups = numGroups

    
    #give user ability to update numGroups w/o having to create a new class
    def setNumGroups(self,numGroups):
        self.numGroups = numGroups
        
    #method to create a starting solution
    def startSol(self,randStart='Y',startMetric=1,seed=1920):
        
        #conditionally create a random or deterministic starting solution
        if randStart == 'Y':
            
            #set random seed
            random.seed(seed)
            
            #create lable list to hold all lables 
            label_list = list(self.df.iloc[:,0])
            
            #instantiate grouping list
            grouping = []

            #initiate first element in each group
            for i in range(0,self.numGroups):
                rand_num = random.randint(0,len(label_list)-1)
                grouping.append([label_list[rand_num]])
                label_list.pop(rand_num)
                
            #loop through each group and add a random element to it until no more elements are left
            while len(label_list) > 1:
                for j in range(0,self.numGroups):
                    #exit loop if label_list becomes too short to avoid out of range errors generated by rand_num
                    if len(label_list) == 1:
                        break
                    rand_num = random.randint(0,len(label_list)-1)
                    grouping[j].append(label_list[rand_num])
                    label_list.pop(rand_num)
                    temp_j = j
            
            #put the last remaining value to the grouping
            grouping[temp_j + 1].append(label_list[0])
                    
                             
        #if not a random starting place, 
        elif randStart == 'N':
            #sort dataframe by startMetric column
            sorted_df = self.df.sort_values(self.startMetric)

            #convert label column in df to list to access .pop() method
            label_list = list(sorted_df.iloc[:,0])
            
            
            #put each element recursively in a group
            grouping = []
            #manually do first iteration to instantiate the appropriate sized list
            for h in range(0,self.numGroups):
                grouping.append([label_list[h]])
            
            #remove elements that were added to grouping in the previous loop
            label_list = label_list[self.numGroups:len(label_list)]

                
            #now that the grouping list is instantiated w/ approprate dimensions, put the rest of the elements into groups
            switch_dir = 1
            
            while len(label_list) > 0:
                if switch_dir == 0:
                
                    #create a varable for looping based on length of lable_list and self.numGroups
                    if len(label_list) < self.numGroups:
                        loop_count = len(label_list)
                    else:
                        loop_count = self.numGroups
                    
                    
                    for i in range(0,loop_count):
                        
                        grouping[i].append(label_list[i])
                        
                    #remove all elements that were just added to the grouping list
                    label_list = label_list[loop_count:len(label_list)]
                            
                    #set switch_dir to 1, so it will loop the opposite direction next while iteration
                    switch_dir = 1
                    print(grouping)
                    
                elif switch_dir == 1:

                    
                    for j in range(self.numGroups-1,-1,-1):
                        print(j)
                        
                        #exit loops if label_list is empty
                        if len(label_list) == 0:
                            break
                            
                        grouping[j].append(label_list[0])
                        label_list.pop(0)
                    
                    
                    #set switch_dir to 0, so it will loop the opposite direction next while iteration
                    switch_dir = 0
                    print(grouping)
        return grouping
    
    
    #create a nieghborhood based on swapping
        #groups input is the solution that needs neighbors
    def createNbrhood(self,groups,nbrHoodSize,numSwaps=1,extraSwapProb=0.1,seed=1920):
        
        #set random seed
        random.seed(seed)
        
        swap_record = []

        nbrHood = []

        for i in range(0,nbrHoodSize):

            #select two groups
            groups_copy = copy.deepcopy(groups)
            group_copy = list(range(0,len(groups)))
            group1 = random.randint(0,len(groups)-1)
            group_copy.pop(group1)

            group2 = random.choice(group_copy)

            #select an element from each group to swap
            swap1 = random.randint(0,len(groups[group1])-1)
            swap2 = random.randint(0,len(groups[group2])-1)

            #create a variable to keep track of changes
            swap_record_temp = [group1,swap1,group2,swap2]


            #check if the swap has already been done before
            if (swap_record_temp not in swap_record):

                #perform swap and save new neighbor in neighbor list
                swap_val1 = groups[group1][swap1]
                swap_val2 = groups[group2][swap2]

                groups_copy[group1][swap1] = swap_val2
                groups_copy[group2][swap2] = swap_val1


                #add the swap to the record of swaps that have been done
                if i == 0:
                    swap_record = [swap_record_temp]
                else:
                    swap_record.append(swap_record_temp)

                #put neighbor into neighborhood list
                nbrHood.append(groups_copy)

        return nbrHood