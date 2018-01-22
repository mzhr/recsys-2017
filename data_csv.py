from baseline import learner, model, parser 

import csv
import random
import time
from collections import Counter
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import pathlib

def sample_targetItems(directory, count):
    (users, items, interactions, 
     target_users, target_items) = learner.baseline_parse(directory)

    pos = int(count * 0.1184)
    neg = count - pos
    neg_set = []
    pos_set = []

    for k in target_items:
        v = items[k]
        if not [len(l) for a, l in v.interacted_with.items() if len(l) > 0]:
            neg_set += [k]
            continue
        else: 
            pos_set += [k]
        if len(pos_set) == pos or len(neg_set) == neg:
            break

    print("NEG COUNT: " + str(len(neg_set)) + " out of " + str(neg))
    print("POS COUNT: " + str(len(pos_set)) + " out of " + str(pos))

    with open("sampled_targetItems.csv", "w", newline='') as f:
        for i in pos_set:
            f.write(str(i) + "\n")
        for i in neg_set:
            f.write(str(i) + "\n")

def item_concept_statistics(directory):
    items_file = directory + "/items.csv"
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    item_no = 0
    concept_stats = {}
    for key, item in items.items():
        if item_no % 100 == 0:
            print("Processing item no: " + str(item_no))
        item_no = item_no + 1

        item_terms = {}
        for c in item.title:
            if c not in item_terms:
                item_terms[c] = 1
        for c in item.tags:
            if c not in item_terms:
                item_terms[c] = 1
        for c, count in item_terms.items():
            if c in concept_stats:
                concept_stats[c] = concept_stats[c] + count
            else:
                concept_stats[c] = count

    with open("item_concept_weights.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in concept_stats.items():
            writeline = []
            writeline.append(str(key))
            writeline.append(str(value))
            csvwriter.writerow(writeline)

def user_concept_statistics(directory):
    users_file = directory + "/users.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))

    user_no = 0
    concept_stats = {}
    for key, user in users.items():
        if user_no % 100 == 0:
            print("Processing item no: " + str(user_no))
        user_no = user_no + 1

        for c in user.jobroles:
            if c in concept_stats:
                concept_stats[c] = concept_stats[c] + 1
            else:
                concept_stats[c] = 1

    with open("user_concept_weights.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in concept_stats.items():
            writeline = []
            writeline.append(str(key))
            writeline.append(str(value))
            csvwriter.writerow(writeline)


def user_interaction_concept_statistics(directory):
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))
    interactions = parser.parse_interactions(interactions_file, users, items)

    interaction_no = 0

    user_stats = {}

    for key, value in interactions.items():
        interaction_no = interaction_no + 1
        if interaction_no % 10000 == 0:
            print("Processing item no: " + str(interaction_no))

        user = key[0]
        item = key[1]
        if user not in user_stats:
                user_stats[user] = {}

        deleted = False
        positive = False
        for i in value.interactions:
            if i.i_type == 4:
                deleted = True
            if i.i_type != 4:
                positive = True

        if deleted == False and positive == True:
            item_terms = {}
            for c in items[item].title:
                if c not in item_terms:
                    item_terms[c] = 1
            for c in items[item].tags:
                if c not in item_terms:
                    item_terms[c] = 1
            for c, count in item_terms.items():
                if c in user_stats[user]:
                    user_stats[user][c] = user_stats[user][c] + count
                else:
                    user_stats[user][c] = count

    with open("user_concept_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for user, concepts in user_stats.items():
            writeline = []
            writeline.append(str(user))
            for c, count in concepts.items():
                writeline.append(str(c))
                writeline.append(str(count))
            csvwriter.writerow(writeline)


def item_interaction_concept_statistics(directory):
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))
    interactions = parser.parse_interactions(interactions_file, users, items)

    interaction_no = 0

    item_stats = {}

    for key, value in interactions.items():
        interaction_no = interaction_no + 1
        if interaction_no % 10000 == 0:
            print("Processing item no: " + str(interaction_no))

        user = key[0]
        item = key[1]
        if item not in item_stats:
                item_stats[item] = {}

        deleted = False
        positive = False
        for i in value.interactions:
            if i.i_type == 4:
                deleted = True
            if i.i_type != 4:
                positive = True

        if deleted == False and positive == True:
            for c in users[user].jobroles:
                if c in item_stats[item]:
                    item_stats[item][c] = item_stats[item][c] + 1
                else:
                    item_stats[item][c] = 1

    with open("item_concept_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for item, concepts in item_stats.items():
            writeline = []
            writeline.append(str(item))
            for c, count in concepts.items():
                writeline.append(str(c))
                writeline.append(str(count))
            csvwriter.writerow(writeline)


def cache_worker(keys, items, users, filename):
    with open(filename, "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dicts = model.data_dicts() 
        count = 0
        data = []
        for key in keys:
            i = items[key[1]]
            u = users[key[0]]
            count += 1
            if (count % 1000000 == 0):
                print("built cache for " + str(count))
            line = []
            interaction = model.Interactions(u, i, [], dicts)
            line.append(key[0])
            line.append(key[1])
            features = list(enumerate(interaction.features(items)))
            line.append(','.join(str((p, a)) for (p, a) in features if a != 0))
            csvwriter.writerow(line)

def build_cache(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items) = learner.baseline_parse(directory)
    n_workers = 47

    pathlib.Path('cache').mkdir(parents=True, exist_ok=True) 

    keys = list(interactions.keys())

    # Schedule classification
    bucket_size = len(keys) / n_workers
    start = 0
    jobs = []
    for i in range(0, n_workers):
        stop = int(min(len(keys), start + bucket_size))
        filename = "cache/cache_" + str(i) + ".csv"
        process = multiprocessing.Process(target = cache_worker,
                                          args=(keys[start:stop],
                                            items, users, filename))
        jobs.append(process)
        start = stop

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    result_file = open("cache/cache.csv", "w") 
    for i in range(0, n_workers):
        filename = "cache/cache_" + str(i) + ".csv"
        tempfile = open(filename, "r")
        result_file.write(tempfile.read() + "\n")

def concept_onehotlist(directory):
    with open("concept_onehot.txt", "w") as f:
        sentence = ""
        for line in open(directory + "/item_concept_weights.csv"):
            newline = line.split() 
            if int(newline[1]) > 500: 
                sentence += newline[1] + ","
            if len(sentence) > 50:
                f.write(sentence+"\n")
                sentence = ""
        f.write(sentence)
        f.write("\n\n]")

        # frequency of concepts
        sentence = ""
        for line in open(directory + "/user_concept_weights.csv"):
            newline = line.split() 
            if int(newline[1]) > 500: 
                sentence += newline[1] + ","
            if len(sentence) > 50:
                f.write(sentence+"\n")
                sentence = ""
        f.write(sentence)


def build_itemitemprofile(self, items):
    users_file = data_directory + "/mode_users.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))

    # Parse interacted data
    print("Parsing interacted with items...")
    for itype in range(6):
        for line in open(user_interactions_file + str(itype) + ".csv"):
            newline = line.split()
            user = int(newline[0])
            users[user].interacted_with[itype] = []
            newline = newline[1:]
            for i in newline:
                users[user].interacted_with[itype] += [int(i)]

    print("Building unbuilt interaction lists...")
    for key, value in users.items():
        for i in range(6):
            if i not in users[key].interacted_with:
                users[key].interacted_with[i] = []
            if i not in users[key].profile:
                users[key].profile[i] = {}

    for i_type in range(6):
        interacted_with = [x for x in self.user.interacted_with[i_type] if x != self.item.id]
        length = len(interacted_with)
        if length == 0:
            continue
        tags = []
        title = []
        clevel = []
        disc = []
        indus = []
        region = []
        country = []
        etype = []
        loc = []
        for i in interacted_with[1:]:
            tags += [items[i].tags]
            title += [items[i].title]
            clevel += [items[i].clevel]
            disc += [items[i].disc]
            indus += [items[i].indus]
            region += [items[i].region]
            country += [items[i].country]
            etype += [items[i].etype]
            features[10 + 12*i_type] += items[i].clevel - self.item.clevel
            features[11 + 12*i_type] += int(self.distance((self.item.lat, self.item.lon), (items[i].lat, items[i].lon)))

    return features

def distance(self, start, end):
    (lat1, lon1) = (start[0], start[1])
    (lat2, lon2) = (end[0], end[1])
    if None in start or None in end:
        return 1000.0
    x = (lon2 - lon1) * math.cos(0.5*(lat2+lat1))
    y = lat2 - lat1
    return 6371 * math.sqrt(x*x + y*y)
