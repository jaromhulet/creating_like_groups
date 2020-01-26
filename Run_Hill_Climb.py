#import modules I made
import base_class as bc
import nbr_hood as nbr
import hill_climb as hc

import pandas as pd

#import data set
test_df = pd.read_csv("C:/Users/jarom/Desktop/DSA 5900/Data/state_data.csv")

#create instance of hillClimb
test = hc.hillClimb(test_df,numGroups=3,nbrhoodsize=100)

#problems with the actual hill climb method and I think there is a problem with random restarts as well.
#results = test2.runHillClimb(selectMethod='FIRST ACCEPT',aggMethod='avg',distMetric='euc',restarts=10)

results = test.runHillClimb(selectMethod='BEST ACCEPT',aggMethod='avg',distMetric='euc',restarts=50)
#results = test.runHillClimb(selectMethod='RANDOM WALK',aggMethod='avg',distMetric='euc',restarts=10,power=3)
#results = test.runVNS(VNS_type='NSWAP',aggMethod='avg',distMetric='euc',restarts=15,nSwaps=2)
#results = test.runVNS(VNS_type='EXPAND',aggMethod='avg',distMetric='euc',restarts=15,expandFactor=5)


print(results[2])
print(results[1])
print(results[3])