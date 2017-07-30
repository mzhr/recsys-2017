#!/usr/bin/env python3

"""
MAZHAR STUFF
"""

from .baseline import xgb, model
import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib

start_time = time.time()

def create_all():
    (users, items, 
     interactions, 
     target_users, 
     target_items) = xgb.baseline_parse("../../data")

def mode_attributes():


# Things to cluster, clevel (0=unknown) itemand suer
# expn expy expc
# edu
# edufos?
# employment type in items
#

#data = np.array([interactions[key].features() for key in interactions.keys()])
clevel_uvector = np.array([u.to_vector() for (k,u) in users.items() if not None in u.to_vector()])
clevel_ivector = np.array([i.to_vector() for (k,i) in items.items() if not None in i.to_vector()])

ukmeans100 = KMeans(n_clusters=100, n_jobs=-1).fit(uvector)
ukmeans200 = KMeans(n_clusters=200, n_jobs=-1).fit(uvector)
ikmeans100 = KMeans(n_clusters=100, n_jobs=-1).fit(ivector)
ikmeans200 = KMeans(n_clusters=200, n_jobs=-1).fit(ivector)
joblib.dump(ukmeans100, 'ukmeans100.pkl') 
joblib.dump(ukmeans200, 'ukmeans200.pkl') 
joblib.dump(ikmeans100, 'ikmeans100.pkl') 
joblib.dump(ikmeans200, 'ikmeans200.pkl') 

###clf = joblib.load('filename.pkl')
print("--- Clustering: %s seconds ---" % (time.time() - start_time))
