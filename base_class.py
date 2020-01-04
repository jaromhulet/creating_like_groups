class baseHeuristic:
    def __init__(self,df):
        
        #df = input dataframe ==> first column must be text identifier, the rest must be numeric
        #distCalc = Type of distance calculation to be used ==> 'euc' = Euclidean, 'man' = Manhattan, 'cos' = cosine
        #aggrMethod = list as long as the columns of df-1, that dictates what kind of aggregation should be done
        #             on a group level ==> 'sum' = add columns by group, 'avg' = get average of columns by group
        
        
        #user input parameters
        self.df = df

        #method created parameters
        self.stdDf = None
        self.aggrDf = None

        #simple calculated parameters
        self.df_len = len(df)
        self.col_ct = len(df.columns)
        self.col_types = self.df.dtypes

        #data validation for df input (dataframe check)
        if isinstance(self.df, pd.DataFrame) == False:
            raise Exception("Input Error: Parameter df must be a pandas dataframe")

        #data validation for df input (check that first column is char and all others are numeric)

        #data validation for distCalc input
        #if self.distCalc not in ['euc','man','cos']:
            #raise Exception("Input Error: Parameter distCalc must be 'euc','man', or 'cos'.")
    
    
        #create a standardized data set when the instance is created
        temp_df = self.df.iloc[:,1:self.col_ct]
        scaler = StandardScaler()
        scaler = scaler.fit_transform(temp_df)
        temp_df = pd.DataFrame(scaler)
        
        #combine standardized data back to label column
        self.stdDf = pd.concat([self.df.iloc[:,0],temp_df],axis=1)
        
    #standardize elements in df
    def standardize(self):
        
        temp_df = self.df.iloc[:,1:self.col_ct]
        scaler = StandardScaler()
        scaler = scaler.fit_transform(temp_df)
        temp_df = pd.DataFrame(scaler)
        
        #combine standardized data back to label column
        self.stdDf = pd.concat([self.df.iloc[:,0],temp_df],axis=1)
        
        return self.stdDf
            
        
    #calculate distance between just two records
    def pairDist(self,a,b,distCalc,):
        
        #convert pandas series to list
        if isinstance(a,pd.core.series.Series) == True:
            a = a.tolist()
        if isinstance(b,pd.core.series.Series) == True:
            b = b.tolist()
        
        #set up variables for the execution of the calculation
        list_len = len(a)
        dist_sum = 0
        temp_dist = 0
        
        #calculate distance based on user self.distCalc (exclude first element in list)
        #Euclidean distance
        if distCalc == 'euc':
            
            for i in range(1,list_len):
                
                temp_dist = (a[i]-b[i])**2
                dist_sum = dist_sum + temp_dist
                
            euc_dist = math.sqrt(dist_sum)
            return euc_dist
                
        #manhattan distance    
        elif distCalc == 'man':
            
            for i in range(1,list_len):
                temp_dist = abs(a[i]-b[i])
                dist_sum = dist_sum + temp_dist
            
            man_dist = dist_sum
            
            return man_dist
        
        #cosine distance
        elif distCalc == 'cos':
            
            #convert to np array
            a = np.asarray(a[:][1:])
            b = np.asarray(b[:][1:])
            
            #calculate dot product
            dot_prod = np.dot(a,b)
            
            #calculate magnitudes
            a_mag = np.linalg.norm(a)
            b_mag = np.linalg.norm(b)
            
            #calculate cosine distance
            cos_dist = dot_prod/(a_mag*b_mag)
            
            return cos_dist
    
    #calculate aggregated metrics by input groups
    def groupMetrics(self,groups,aggMethod):
        #Instantiate master list to hold aggregated metrics by group
        master_list = []
        
        #iterate through all groups -- groups will come from the hueristic portion of the programming
        for i in range(0,len(groups)):
            temp_group = groups[i]
            temp_df = self.stdDf[self.stdDf.iloc[:,0].isin(temp_group)]

            #start temp_list with group number
            temp_list = [i]
            #iterate through columns at a group level
            for j in range(0,(len(self.stdDf.columns)-1)):

                #if user input list of aggregation types is 'sum', then execute
                if aggMethod[j] == 'sum':
                    #calculate column sum
                    temp_aggr = temp_df.iloc[:,j+1].sum()
                    #append summed value to list
                    temp_list.append(temp_aggr)

                #if user input list of aggregation types is 'avg', then execute
                elif aggMethod[j] == 'avg':
                    #calculate column mean
                    temp_aggr = temp_df.iloc[:,j+1].mean()
                    #append mean value to list
                    temp_list.append(temp_aggr)
                #put temp_list in master_list once all columns for the group have been aggregated
            master_list.append(temp_list)

            #convert master list into dataframe
            master_df = pd.DataFrame(master_list)
            
            #set self.aggrDf attribute equal to the aggregated group dataframe
            self.aggrDf = master_df
            
        return master_df

    #add up all of the pairwise distances using pairDist method
    def totalDist(self):
        
        row_num = len(self.aggrDf)
        combins = list(combinations(list(range(0,row_num)),2))

        #instantiac variable to hold total distance
        total_dist = 0
        
        for i in range(0,len(combins)):

            temp_dist_df = self.aggrDf[self.aggrDf.iloc[:,0].isin(combins[i])]
            
            #Get pairwise distance between two groups at a time, using self.pairDist
            temp_dist = self.pairDist(self.aggrDf.iloc[0,:],self.aggrDf.iloc[1,:])
            
            #add to total_dist
            total_dist = total_dist + temp_dist
        
        return total_dist