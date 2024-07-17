# -*- coding: utf-8 -*-
"""

@author: Bannikov Maxim
"""

from __future__ import print_function, division
import numpy as np
from flask import Flask, jsonify, request
from scipy.stats import gamma
from matplotlib import pyplot as plt

app = Flask(__name__)

class Bandit:
  def __init__(self, name):
    self.name = name
    self.n_prior = 2
    self.df_prior = 2 - 1 
    self.var_prior = ((1-0)*2)**2
    self.mean_prior = (1-0)/2
    self.n_sample = 0
    self.var_sample = self.var_prior
    self.sum_sample = [self.mean_prior for x in np.arange(1,self.n_prior+1)]
    self.df_post = self.df_prior
    self.n_post = self.n_prior
    
  def sample(self):
    return np.random.normal(self.mean_post,self.var_post)

  def update(self,x):
    self.n_sample += 1
    self.sum_sample.append(x)
    self.mean_sample = np.mean(self.sum_sample)
    self.var_sample = np.var(self.sum_sample)
    
    self.df_post += 1
    self.n_post += 1    
    self.mean_post =  (self.n_sample*self.mean_sample + self.n_prior*self.mean_prior)/self.n_post
    self.var_post = ((self.n_sample-1)*self.var_sample + self.df_prior*self.var_prior + self.n_prior*self.n_sample*(self.mean_prior - self.mean_sample)**2/self.n_post)/self.df_post
      
def plot(bandits,trial):
  x = np.linspace(0, 1, 200)
  for b in bandits:
     y = gamma.pdf(x,b.a,b.b)
     plt.plot(x,y,label=f"win rate = {b.a - 1}/{b.N}")
     plt.title(f"Bandit distributions after {trial} trials")
  plt.legend()
  plt.show()
  
class Trials:
    def __init__(self):
        self.c = 0
    
    def update(self):
        self.c +=1
    
    def count(self):
        return self.c

# initialize bandits
bandit_names = ['A','B']
bandits = [Bandit(p) for p in bandit_names]
sample_points = [10,20,30,40,50,100,200,500,1000,1999]
Count_trials = Trials()

@app.route('/get_ad')
def get_ad():
    
  max_index = np.argmax([b.sample() for b in bandits])
  ad_pull = bandits[max_index].name
  bandits[max_index].update(0)
  Count_trials.update()
  
  if Count_trials.count() in sample_points:
    plot(bandits, Count_trials.count())
  
  return jsonify({'advertisement_id': ad_pull})


@app.route('/click_ad', methods=['POST'])
def click_ad():
    
  result = 'OK'
  ad_name = request.form['advertisement_id']
  
  if np.isin(ad_name,bandit_names):
    for b in bandits:
      if b.name == ad_name:
         b.update(1)
  else:
    result = 'Invalid Input.'

  # nothing to return really
  return jsonify({'result': result})

if __name__ == '__main__':
  app.run(host='127.0.0.1', port='8888')