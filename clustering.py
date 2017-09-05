from baseline import learner, model, parser

import time
import csv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib


def cluster(directory):
    (header_users, users) = parser.select(directory + "/users.csv", lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(directory + "/items.csv", lambda x: True, parser.build_item, lambda x: int(x[0]))

    (user_values, item_values) = get_attributes(users, items)
    (mode_users, mode_items) = mode_attributes(user_values, item_values, users, items)    
    write_values(mode_users, mode_items, header_users, header_items)

def mode_attributes(user_values, item_values, users, items):
    user_stats = [[],[],[],[]]
    item_stats = [[],[],[],[],[],[]]
    
    print("Counting values")
    for user, value in user_values.items():
        user_stats[0] += [value[1]]
        user_stats[1] += [value[2]]
        user_stats[2] += [value[3]]
        user_stats[3] += [value[7]]

    for item, value in item_values.items():
        item_stats[0] += [value[2]]
        item_stats[1] += [value[3]]
        item_stats[2] += [value[4]]
        item_stats[3] += [value[8]]
        item_stats[4] += [value[9]]
        item_stats[5] += [value[10]]

    print("Finding mode of values")
    for i in range(len(user_stats)):
        filtered = [v for v in user_stats[i] if v != 0]
        data = Counter(filtered)
        user_stats[i] = data.most_common()[0][0]

    for i in range(len(item_stats)):
        filtered = [v for v in item_stats[i] if v != 0]
        data = Counter(filtered)
        item_stats[i] = data.most_common()[0][0]

    print(user_stats)
    print(item_stats)

    print("altering user and item dataset")
    for user, value in users.items():
        if value.clevel == 0:
            users[user].clevel = user_stats[0]
        if value.disc == 0:
            users[user].disc = user_stats[1]
        if value.indus == 0:
            users[user].indus = user_stats[2]
        if value.edud == 0:
            users[user].edud = user_stats[3]

    for item, value in items.items():
        if value.disc == 0:
            items[item].disc = item_stats[0]
        if value.indus == 0:
            items[item].indus = item_stats[1]
        if value.clevel == 0:
            items[item].clevel = item_stats[2]
        if value.lat == 0:
            items[item].lat = item_stats[3]
        if value.lon == 0:
            items[item].lon = item_stats[4]
        if value.etype == 0:
            items[item].etype = item_stats[5]

    return (users, items)

"""
def clustered_attributes(users, items):
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
"""

def get_attributes(users, items):
    user_values = {}
    item_values = {}
    c = {"de": 0, "at": 1, "ch": 2, "non_dach": 3}

    print("preprocessing data")
    for user, value in users.items():
        user_values[user] = []
        user_values[user] += [value.jobroles]
        user_values[user] += [value.clevel]
        user_values[user] += [value.disc]
        user_values[user] += [value.indus]
        user_values[user] += [value.expn]
        user_values[user] += [value.expy]
        user_values[user] += [value.expyc]
        user_values[user] += [value.edud]
        user_values[user] += [value.edufos]
        user_values[user] += [c[value.country]]
        user_values[user] += [value.region]
        user_values[user] += [value.xtcj]
        user_values[user] += [value.premium]

    for item, value in items.items():
        item_values[item] = []
        item_values[item] += [value.title]
        item_values[item] += [value.tags]
        item_values[item] += [value.disc]
        item_values[item] += [value.indus]
        item_values[item] += [value.clevel]
        item_values[item] += [c[value.country]]
        item_values[item] += [value.region]
        item_values[item] += [value.paid]
        item_values[item] += [value.lat]
        item_values[item] += [value.lon]
        item_values[item] += [value.etype]
        item_values[item] += [value.time]

    return (user_values, item_values)



def write_values(users, items, user_header, item_header):
    print("writing values")
    with open("mode_users.csv", "w", newline='') as user_f:
        csvwriter = csv.writer(user_f, delimiter='\t', quoting=csv.QUOTE_NONE)
        line = []
        for h, v in user_header.items():
            line.append("recsyschallenge_v2017_users_final_anonym_export_unique." + h)
        csvwriter.writerow(line)

        for user, value in users.items():
            line = []
            line.append(str(value.id))
            line.append(','.join(str(a) for a in value.jobroles))
            line.append(str(value.clevel))
            line.append(str(value.disc))
            line.append(str(value.indus))
            line.append(str(value.country))
            line.append(str(value.region))
            line.append(str(value.expn))
            line.append(str(value.expy))
            line.append(str(value.expyc))
            line.append(str(value.edud))
            line.append(','.join(str(a) for a in value.edufos))
            line.append(str(value.xtcj))
            line.append(str(value.premium))
            csvwriter.writerow(line)

    with open("mode_items.csv", "w", newline='') as item_f:
        csvwriter = csv.writer(item_f, delimiter='\t', quoting=csv.QUOTE_NONE)
        line = []
        for h, v in item_header.items():
               line.append("recsyschallenge_v2017_items_final_training_export." + h)
        csvwriter.writerow(line)

        for item, value in items.items():
            line = []
            line.append(str(value.id))
            line.append(','.join(str(a) for a in value.title))
            line.append(str(value.clevel))
            line.append(str(value.disc))
            line.append(str(value.indus))
            line.append(str(value.country))
            line.append(str(value.paid))
            line.append(str(value.region))
            line.append(str(value.lat))
            line.append(str(value.lon))
            line.append(str(value.etype))
            line.append(','.join(str(a) for a in value.tags))
            line.append(str(value.time))
            csvwriter.writerow(line)




    
