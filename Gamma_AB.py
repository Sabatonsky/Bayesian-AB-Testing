# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:27:56 2022

@author: Bannikov Maxim
"""

import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('advertisement_clicks.csv')
df_a = df[df.advertisement_id == 'A']

var_real = np.var(df_a)[0]
mean_real = np.mean(df_a)[0]

n_prior = 2
df_prior = 2 - 1 
var_prior = ((1-0)*2)**2
mean_prior = (1-0)/2

n_sample = 0
var_sample = var_prior
sum_sample = [mean_prior for x in np.arange(1,n_prior+1)]

df_post = df_prior
n_post = n_prior

sample_points = [0,1,2,3,4,5,10,20,50,100,200,300,400,500,600,700,800,900,999]

for i, row in enumerate(df_a.values):
    
    n_sample += 1
    sum_sample.append(row[1])
    mean_sample = np.mean(sum_sample)
    var_sample = np.var(sum_sample)
    
    df_post += 1
    n_post += 1    
    mean_post = (n_sample*mean_sample + n_prior*mean_prior)/n_post
    var_post = ((n_sample-1)*var_sample + df_prior*var_prior + n_prior*n_sample*(mean_prior - mean_sample)**2/n_post)/df_post
    
    if i in sample_points:
        x = np.linspace(0,1,200)
        y = norm.pdf(x, mean_post, var_post)
        plt.title(f"Distribution after {n_sample} trials")
        plt.plot(x,y,label = f"Variance = {var_post:.2f} Mean = {mean_post:.2f}")
        plt.legend()
        plt.show()
        