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

    #(mode_users, mode_items) = mode_attributes(users, items)    
    #write_values(mode_users, mode_items, header_users, header_items, "mode_users.csv", "mode_items.csv")
  
    (mode_users, mode_items) = clustered_attributes(5, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k5_clustered_users.csv", "k5_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(10, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k10_clustered_users.csv", "k10_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(20, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k20_clustered_users.csv", "k20_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(30, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k30_clustered_users.csv", "k30_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(50, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k50_clustered_users.csv", "k50_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(100, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k100_clustered_users.csv", "k100_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(200, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k200_clustered_users.csv", "k200_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(300, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k300_clustered_users.csv", "k300_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(500, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k500_clustered_users.csv", "k500_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(1000, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k1000_clustered_users.csv", "k1000_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(2000, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k2000_clustered_users.csv", "k2000_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(3000, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k3000_clustered_users.csv", "k3000_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(5000, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k5000_clustered_users.csv", "k5000_clustered_items.csv")
    (mode_users, mode_items) = clustered_attributes(10000, users, items)
    write_values(mode_users, mode_items, header_users, header_items, "k10000_clustered_users.csv", "k10000_clustered_items.csv")
  

def mode_attributes(users, items):
    user_stats = [[],[],[],[],[],[],[],[],[]]
    item_stats = [[],[],[],[],[],[],[],[]]
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
    for i in range(len(user_stats)):
        filtered = [v for v in user_stats[i] if v != 0]
        data = Counter(filtered)
        print(data.most_common())
        user_stats[i] = data.most_common()[0][0]

    for i in range(len(item_stats)):
        filtered = [v for v in item_stats[i] if v != 0]
        data = Counter(filtered)
        item_stats[i] = data.most_common()[0][0]

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

    for item, value in items.items():
        if value.disc == 0:
            items[item].disc = item_stats[0]
        if value.indus == 0:
            items[item].indus = item_stats[1]
        if value.clevel == 0:
            items[item].clevel = item_stats[2]
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

    return (users, items)


def clustered_attributes(k, users, items):
    cntry = {"de": 1, "at": 2, "ch": 3, "non_dach": 0}
    user_stats = []
    item_stats = []

    print("Counting values Users")
    for user, value in users.items():
        d = [value.clevel, value.disc, value.indus, 
             value.expn, value.expy, value.expyc, 
             value.edud, cntry[value.country], value.region]
        if 0 not in d:
            user_stats += [d]

    print("Counting values Items")
    for item, value in items.items():
        d = [value.clevel, value.disc, value.indus, 
             cntry[value.country], value.region,
             value.lat, value.lon, value.etype]
        if d[5] == None:
            d[5] = 0
        if d[6] == None:
            d[6] = 0
        if 0 not in d:
            item_stats += [d]

    #data = np.array([interactions[key].features() for key in interactions.keys()])
    users_vector = np.array(user_stats)
    items_vector = np.array(item_stats)

    start_time = time.time()

    ucluster5 = KMeans(n_clusters=k, n_jobs=-1, verbose=1).fit(users_vector)
    icluster5 = KMeans(n_clusters=k, n_jobs=-1, verbose=1).fit(items_vector)

    print("--- Clustering: %s seconds ---" % (time.time() - start_time))

    finding_time = time.time()
    ucluster_members = {}
    icluster_members = {}
    for i in range(k):
        ucluster_members[i] = {}
        icluster_members[i] = {}

    print("Finding cluster groups for users")
    for u, value in users.items():
        d = [value.clevel, value.disc, value.indus, 
             value.expn, value.expy, value.expyc, 
             value.edud, cntry[value.country], value.region]
        c = ucluster5.predict(d)
        ucluster_members[c[0]][u] = value

    print("finding cluster groups for items")
    for i, value in items.items():
        d = [value.clevel, value.disc, value.indus, 
            cntry[value.country], value.region, 
            value.lat, value.lon, value.etype]
        if d[5] == None:
            d[5] = 0
        if d[6] == None:
            d[6] = 0
        c = icluster5.predict(d)
        icluster_members[c[0]][i] = value

    print("--- Estimating: %s seconds ---" % (time.time() - finding_time))

    estimate_time = time.time()
    print("Setting values Values")
    final_users = {}
    final_items = {}
    for i in range(k):
        (mode_users, mode_items) = mode_attributes(ucluster_members[i], icluster_members[i])    
        s = {**final_users, **mode_users}
        final_users = s
        p = {**final_items, **mode_items}
        final_items = p

    print("--- Estimating: %s seconds ---" % (time.time() - estimate_time))
    return (final_users, final_items)

def write_values(users, items, user_header, item_header, uname, iname):
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




    
