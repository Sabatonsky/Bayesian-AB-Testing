# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:37:47 2022

@author: Bannikov Maxim
"""
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd

class Bandit:
  def __init__(self, name):
    self.name = name
    self.mean = 0
    self.prc = 1
    self.N = 0
    
  def sample(self):
    return np.random.normal(self.mean, 1/self.prc)

  def update_gamma(self,x):
    self.a += x
    self.b += 1-2*x
    self.N += 1-x

x = np.linspace(-5, 5, 200)
y = norm.pdf(x,0,1)
plt.plot(x,y)
plt.show()
  
df = pd.read_csv('advertisement_clicks.csv')
df_a = df[df.advertisement_id == 'A']
df_b = df[df.advertisement_id == 'B']
prc_a = 1/np.var(df_a)[0]
prc_b = 1/np.var(df_b)[0]
