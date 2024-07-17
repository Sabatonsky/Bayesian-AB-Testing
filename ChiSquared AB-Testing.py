# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:10:27 2022

@author: Bannikov Maxim
"""

import numpy as np
import pandas as pd
from scipy import stats

ads_clicks_df= pd.read_csv('advertisement_clicks.csv')
a_df= ads_clicks_df[ads_clicks_df['advertisement_id']=='A']
b_df= ads_clicks_df[ads_clicks_df['advertisement_id']=='B']

a_s=a_df.loc[a_df['action']==1,'action'].count()
a_f=a_df.loc[a_df['action']==0,'action'].count()
b_s=b_df.loc[b_df['action']==1,'action'].count()
b_f=b_df.loc[b_df['action']==0,'action'].count()

chi_stat = (a_s+b_f+a_f+b_s)*(a_s*b_f-a_f*b_s)**2/((a_s+a_f)*(b_s+b_f)*(a_s+b_s)*(a_f+b_f))
p = 1 - stats.chi2.cdf(np.abs(chi_stat),df=1)

print("ChiSquared-test")
print("p:\t", p)