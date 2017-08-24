from baseline import learner, model

import csv
import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib


def minify_interactions(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items) = learner.baseline_parse(directory)

    interactions = {}

    for line in open(directory + "/interactions.csv"):
        newline = line.strip()
        if (newline[0], newline[1]) not in interactions:
            interactions[(newline[0], newline[1])] = []
        else:
            interactions[(newline[0], newline[1])].append(
                    (newline[2], newline[3])) 

    with open("minified_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in interactions.items():
            writeline = []
            writeline.append(key)
            for i in value:
                writeline.append(i[0])
                writeline.append(i[1])
            csvwriter.writerow(writeline)


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
