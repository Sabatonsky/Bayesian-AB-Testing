# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:10:27 2022

@author: Bannikov Maxim
"""

PtrueCA=0.019/(0.019+0.28)
PfalseCA=0.28/(0.019+0.28)
ptest=1/(2**1024)

import numpy as np
from scipy import stats
import pandas as pd

ads_clicks_df = pd.read_csv('advertisement_clicks.csv')

ads_clicks_df.iloc[:,0].astype("category")

a_df = ads_clicks_df[ads_clicks_df['advertisement_id']=='A']
b_df = ads_clicks_df[ads_clicks_df['advertisement_id']=='B']

ads_clicks_df.dtypes

t, p = stats.ttest_ind(a_df['action'], b_df['action'])

a = len(a_df['advertisement_id'])
b = len(b_df['advertisement_id'])

var_a = a_df['action'].var()
var_b = b_df['action'].var()

test = (a_df['action'].mean() - b_df['action'].mean())/np.sqrt(var_a/a + var_b/b)

nu1 = a - 1
nu2 = b - 1
df = (var_a / a + var_b/ b)**2 / ( (var_a**2) / (a**2 * nu1) + (var_b**2) / (b**2 * nu2))
p = (1 - stats.t.cdf(np.abs(test), df=df))*2
print("Manual Welch t-test")
print("t:\t", t, "p:\t", p)
