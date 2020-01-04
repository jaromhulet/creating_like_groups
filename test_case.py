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

print(test.df_len)

print('done')


