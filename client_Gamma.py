"""
@author: Bannikov Maxim

"""
from __future__ import print_function, division

import requests
import numpy as np

# get data
rng = np.random.default_rng()
a = rng.normal(1000, 250, 2000)
b = rng.normal(980, 250, 2000)

print("a.mean:", a.mean())
print("b.mean:", b.mean())

i = 0
j = 0
count = 0
while i < len(a) and j < len(b):
  # quit when there's no data left for either ad
  r = requests.get('http://localhost:8888/get_site')
  # print(r.content)
  r = r.json()
  if r['site_id'] == 'A':
    check = a[i]
    i += 1
  else:
    check = b[j]
    j += 1

  requests.post(
      'http://localhost:8888/checkout',
      data={'site_id': r['site_id'],'check': check}
  )

  # log some stats
  count += 1
  if count % 50 == 0:
    print("Site visits %s, A: %s, B: %s" % (count, i, j))
