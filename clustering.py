from baseline import learner, model, parser

import time
import csv
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib


def cluster(directory):
    (header_items, items) = parser.select(directory + "/items.csv", lambda x: True, parser.build_item, lambda x: int(x[0]))
    mode_i = clustered_items(10000, items)
    write_items(mode_i, header_items, "tclustered_items.csv")

    (header_users, users) = parser.select(directory + "/users.csv", lambda x: True, parser.build_user, lambda x: int(x[0]))
    mode_u = clustered_users(10000, users)
    write_users(mode_u, header_users, "tclustered_users.csv")
  
def mode_users(users):
    user_stats = [[],[],[],[],[],[],[],[],[]]
    cntry = {"de": 1, "at": 2, "ch": 3, "non_dach": 0}
    inv_cntry = {1: "de", 2: "at", 3: "ch", 0: "non_dach"}

    print("Counting values")
    for user, value in users.items():
        user_stats[0] += [value.clevel]
        user_stats[1] += [value.disc]
        user_stats[2] += [value.indus]
        user_stats[3] += [value.expn]
        user_stats[4] += [value.expy]
        user_stats[5] += [value.expyc]
        user_stats[6] += [value.edud]
        user_stats[7] += [cntry[value.country]]
        user_stats[8] += [value.region]

    print("Finding mode of values")
    for i in range(len(user_stats)):
        filtered = [v for v in user_stats[i] if v != 0]
        data = Counter(filtered)
        user_stats[i] = data.most_common()[0][0]

    print("altering user and item dataset")
    for user, value in users.items():
        if value.clevel == 0:
            users[user].clevel = user_stats[0]
        if value.disc == 0:
            users[user].disc = user_stats[1]
        if value.indus == 0:
            users[user].indus = user_stats[2]
        if value.expn == 0:
            users[user].expn = user_stats[3]
        if value.expy == 0:
            users[user].expy = user_stats[4]
        if value.expyc == 0:
            users[user].expyc = user_stats[5]
        if value.edud == 0:
            users[user].edud = user_stats[6]
        if value.country == "non_dach":
            users[user].country = inv_cntry[user_stats[7]]
        if value.region == 0:
            users[user].region = user_stats[8]

    return users


def mode_items(items):
    item_stats = [[],[],[],[],[],[],[],[]]
    cntry = {"de": 1, "at": 2, "ch": 3, "non_dach": 0}
    inv_cntry = {1: "de", 2: "at", 3: "ch", 0: "non_dach"}
    
    print("Counting values")
    for item, value in items.items():
        item_stats[0] += [value.clevel]
        item_stats[1] += [value.disc]
        item_stats[2] += [value.indus]
        item_stats[3] += [cntry[value.country]]
        item_stats[4] += [value.region]
        if value.lat == None:
            item_stats[5] += [0]
        else:
            item_stats[5] += [value.lat]
        if value.lon == None:
            item_stats[6] += [0]
        else:
            item_stats[6] += [value.lon]
        item_stats[7] += [value.etype]

    print("Finding mode of values")
    for i in range(len(item_stats)):
        filtered = [v for v in item_stats[i] if v != 0]
        data = Counter(filtered)
        item_stats[i] = data.most_common()[0][0]

    print("altering user and item dataset")
    for item, value in items.items():
        if value.clevel == 0:
            items[item].clevel = item_stats[0]
        if value.disc == 0:
            items[item].disc = item_stats[1]
        if value.indus == 0:
            items[item].indus = item_stats[2]
        if value.country == "non_dach":
            items[item].country = inv_cntry[item_stats[3]]
        if value.region == 0:
            items[item].region = item_stats[4]
        if value.lat == None:
            items[item].lat = item_stats[5]
        if value.lon == None:
            items[item].lon = item_stats[6]
        if value.etype == 0:
            items[item].etype = item_stats[7]

    return items


def clustered_users(k, users):
    cntry = {"de": 1, "at": 2, "ch": 3, "non_dach": 0}
    user_stats = []

    print("Counting values Users")
    for user, value in users.items():
        f_list = [0]*100
        f_list[value.clevel] = 1
        f_list[7+value.disc] = 1
        f_list[31+value.indus] = 1
        f_list[55+value.expn] = 1
        f_list[59+value.expy] = 1
        f_list[66+value.expyc] = 1
        f_list[73+value.edud] = 1
        f_list[77+value.region] = 1
        f_list[94+value.xtcj] = 1
        f_list[96+cntry[value.country]] = 1
        d = [value.clevel, value.disc, value.indus, 
             value.expn, value.expy, value.expyc, 
             value.edud, cntry[value.country], value.region]
        if 0 not in d:
            user_stats += [f_list]

    print("Clustering")
    users_vector = np.array(user_stats)
    ucluster5 = KMeans(n_clusters=k, n_jobs=-1).fit(users_vector)

    print("Finding cluster groups for users")
    ucluster_members = {}
    for i in range(k):
        ucluster_members[i] = {}

    for u, value in users.items():
        f_list = [0]*100
        f_list[value.clevel] = 1
        f_list[7+value.disc] = 1
        f_list[31+value.indus] = 1
        f_list[55+value.expn] = 1
        f_list[59+value.expy] = 1
        f_list[66+value.expyc] = 1
        f_list[73+value.edud] = 1
        f_list[77+value.region] = 1
        f_list[94+value.xtcj] = 1
        f_list[96+cntry[value.country]] = 1
        c = ucluster5.predict(f_list)
        ucluster_members[c[0]][u] = value

    print("Setting values Values")
    final_users = {}
    for i in range(k):
        mode = mode_users(ucluster_members[i])    
        s = {**final_users, **mode}
        final_users = s

    return final_users

def clustered_items(k, items):
    cntry = {"de": 1, "at": 2, "ch": 3, "non_dach": 0}
    item_stats = []

    print("Counting values Items")
    for item, value in items.items():
        lat = value.lat
        lon = value.lon
        if value.lat == None:
            lat = 0
        if value.lon == None:
            lon = 0
        f_list = [0]*85
        f_list[value.clevel] = 1
        f_list[7+value.disc] = 1
        f_list[31+value.indus] = 1
        f_list[55+value.paid] = 1
        f_list[57+value.etype] = 1
        f_list[61+value.region] = 1
        f_list[78+cntry[value.country]] = 1
        f_list[82] = lat
        f_list[83] = lon
        d = [value.clevel, value.disc, value.indus, 
             cntry[value.country], value.region,
             lat, lon, value.etype]
        if 0 not in d:
            item_stats += [f_list]

    print("Clustering")
    items_vector = np.array(item_stats)
    icluster5 = KMeans(n_clusters=k, n_jobs=-1).fit(items_vector)

    icluster_members = {}
    for i in range(k):
        icluster_members[i] = {}

    print("finding cluster groups for items")
    for i, value in items.items():
        lat = value.lat
        lon = value.lon
        if value.lat == None:
            lat = 0
        if value.lon == None:
            lon = 0
        f_list = [0]*85
        f_list[value.clevel] = 1
        f_list[7+value.disc] = 1
        f_list[31+value.indus] = 1
        f_list[55+value.paid] = 1
        f_list[57+value.etype] = 1
        f_list[61+value.region] = 1
        f_list[78+cntry[value.country]] = 1
        f_list[82] = lat
        f_list[83] = lon
        c = icluster5.predict(f_list)
        icluster_members[c[0]][i] = value

    print("Setting values Values")
    final_users = {}
    final_items = {}
    for i in range(k):
        mode = mode_items(icluster_members[i])    
        p = {**final_items, **mode}
        final_items = p

    return final_items

def write_users(users, user_header, uname):
    print("writing values")
    with open(uname, "w", newline='') as user_f:
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


def write_items(items, item_header, iname):
    print("writing values")
    with open(iname, "w", newline='') as item_f:
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

