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
test = hc.hillClimb(test_df,3)

#problems with the actual hill climb method and I think there is a problem with random restarts as well.
#results = test.runHillClimb(selectMethod='First Accept',aggMethod='avg',distMetric='euc',restarts=3)

results = test.runHillClimb(selectMethod='TEST2',aggMethod='avg',distMetric='euc',restarts=25)

print("done on main")
print(results[2])



