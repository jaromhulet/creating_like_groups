import pandas as pd
from sklearn.preprocessing import StandardScaler
import math
import numpy as np
from itertools import combinations
import random 

#import modules I made
import base_class as bc
import nbr_hood as nbr
import hill_climb as hc

#import data set
test_df = pd.read_csv("C:/Users/jarom/Desktop/DSA 5900/Data/state_data.csv")

#create baseHeuristic instance
test = hc.hillClimb(test_df,numGroups=3,nbrhoodsize=10)

#problems with the actual hill climb method and I think there is a problem with random restarts as well.
#results = test.runHillClimb(selectMethod='FIRST ACCEPT',aggMethod='avg',distMetric='euc',restarts=20)
#results = test.runHillClimb(selectMethod='BEST ACCEPT',aggMethod='avg',distMetric='euc',restarts=15)
#results = test.runHillClimb(selectMethod='RANDOM WALK',aggMethod='avg',distMetric='euc',restarts=10,power=3)

results = test.runVNS(VNS_type='NSWAP',aggMethod='avg',distMetric='euc',restarts=15,nSwaps=2)

#summary = test.sample_hist(20000,aggMethod='avg',distMetric='euc',bin_count=100)


#print(summary)
print("done on main")
print(results[2])
print(results[1])
print(results[3])



