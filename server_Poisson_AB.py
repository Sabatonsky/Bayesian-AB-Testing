"""
@author: Bannikov Maxim

"""
from __future__ import print_function, division

import numpy as np
from flask import Flask, jsonify, request
from scipy.stats import poisson
from scipy.stats import nbinom
from matplotlib import pyplot as plt

app = Flask(__name__)

class Bandit:
  def __init__(self, name):
    self.name = name
    self.sum = 2000
    self.base = 1
    
  def sample(self):
    return np.random.gamma(self.sum, 1/self.base)

  def update(self,x):
    self.sum += x
    self.base += 1

def plot(bandits, trial):
  for b in bandits:
     n = b.sum
     p = (b.base)/(b.base+1)
     x = np.arange(poisson.ppf(0.01, 1000), poisson.ppf(0.99, 1000))
     y = nbinom.pmf(x, n, p)
     plt.plot(x, y, label=f"avg check = {round(b.sum/b.base)}")
     plt.title(f"Bandit distributions after {trial} trials")
     
  plt.plot(x, poisson.pmf(x, 1000), label="poisson avg 1000")  
  plt.plot(x, poisson.pmf(x, 980), label="poisson avg 980")      
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

@app.route('/get_site')
def get_site():
  
  max_index = np.argmax([b.sample() for b in bandits])
  site_pull = bandits[max_index].name
  Count_trials.update()
  
  if Count_trials.count() in sample_points:
    plot(bandits, Count_trials.count())
  
  return jsonify({'site_id': site_pull})


@app.route('/checkout', methods=['POST'])
def checkout():
    
  result = 'OK'
  site_name = request.form['site_id']
  
  if np.isin(site_name,bandit_names):
    for b in bandits:
      if b.name == site_name:
         b.update(int(request.form['check']))
  else:
    result = 'Invalid Input.'

  # nothing to return really
  return jsonify({'result': result})


if __name__ == '__main__':
  app.run(host='127.0.0.1', port='8888')
