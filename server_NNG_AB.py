"""
@author: Bannikov Maxim

"""
from __future__ import print_function, division

import numpy as np
import math
from flask import Flask, jsonify, request
from scipy.stats import norm
from scipy.stats import t
from matplotlib import pyplot as plt

app = Flask(__name__)

class Bandit:
    def __init__(self, name):
        self.name = name
        self.mu = 2000
        self.n = 2    
        self.a = 0.5*self.n
        self.b = 0.5*(self.mu/4)**2
        self.prc = 0
    
    def sample(self):
        self.prc = np.random.gamma(self.a, 1/self.b)
        return np.random.normal(self.mu, (1/(self.prc*self.n))**0.5)

    def update(self,x):
        self.b = self.b + 0.5*self.n*(x-self.mu)**2/(self.n+1)
        self.mu = (self.n*self.mu+x)/(self.n+1)
        self.a += 0.5
        self.n += 1

def plot(bandits, trial):
    for b in bandits:
        mean = b.mu
        var = b.b*(b.n+1)/(b.a*b.n)
        x = np.linspace(t.ppf(0.01, 1000, loc = 1000, scale = 250), t.ppf(0.99, 1000, loc = 1000, scale = 250), 100)
        y = t.pdf(x, df = 2*b.a, loc = mean, scale = math.sqrt(var))
        plt.plot(x, y, label=f"mean = {round(mean)}; var = {round(math.sqrt(var))}")
        plt.title(f"Bandit distributions after {trial} trials")

        y = norm.pdf(x, loc = b.mu, scale = math.sqrt(1/(b.prc*b.n)))
        plt.plot(x, y, label=f"mean = {round(b.mu)}; var = {round(math.sqrt(1/(b.prc*b.n)))}")
        
    plt.plot(x, norm.pdf(x, loc = 1000, scale = 100), label="z-dist avg 1000, std 100")  
    plt.plot(x, norm.pdf(x, loc = 980, scale = 100), label="z-dist avg 980, std 100")      
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
         b.update(float(request.form['check']))
  else:
    result = 'Invalid Input.'

  # nothing to return really
  return jsonify({'result': result})


if __name__ == '__main__':
  app.run(host='127.0.0.1', port='8888')
