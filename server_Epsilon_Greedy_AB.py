"""
@author: Bannikov Maxim

"""
from __future__ import print_function, division
import numpy as np
from flask import Flask, jsonify, request

# create an app
app = Flask(__name__)

class Bandit:
  def __init__(self, name):
    self.name = name
    self.a = 0
    self.N = 0
    
  def exploit(self):
    return self.a/self.N
    
  def explore(self):
      return np.random.random()

  def update(self,x):
    self.a += x
    self.N += 1-x
  
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
sample_points = np.arange(50,1500,50)
Count_trials = Trials()

@app.route('/get_ad')
def get_ad():
    
  min_pull = np.argmin([b.N for b in bandits])

  if bandits[min_pull].N < 10:
    bandits[min_pull].update(0)
    ad_pull = bandits[min_pull].name              
  else:
    if np.random.random() < 0.1: 
      max_index = np.argmax([b.explore() for b in bandits])
    else:
      max_index = np.argmax([b.exploit() for b in bandits])
    bandits[max_index].update(0)
    ad_pull = bandits[max_index].name

    
  Count_trials.update()
  
  if Count_trials.count() % 50 == 0:
      
    i = np.array([b.a for b in bandits])
    j = np.array([b.N for b in bandits])
    string_array = np.array2string(np.divide(i,j), separator=',', formatter={'float_kind':lambda x: "%.2f" % x})
    print("Seen %s ads, Probabilities: %s" % (Count_trials.count(), string_array))
  
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