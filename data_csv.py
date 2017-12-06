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

def minify_interactions(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = {}

    with open(directory + "/interactions.csv") as fo:
        next(fo)
        for line in fo:
            newline = line.strip().split()
            if (int(newline[0]), int(newline[1])) not in interactions:
                interactions[(int(newline[0]), int(newline[1]))] = [(int(newline[2]), int(newline[3]))]
            else:
                interactions[(int(newline[0]), int(newline[1]))].append(
                        (int(newline[2]), int(newline[3]))) 

    with open("minified_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for key, value in interactions.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            writeline = []
            writeline.append(key[0])
            writeline.append(key[1])
            for i in sort:
                writeline.append(i[0])
                writeline.append(i[1])
            csvwriter.writerow(writeline)


def sampled_interactions(directory, p_count, n_count):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"
    user_interactions_file = directory + "/user_interactions"
    item_interactions_file = directory + "/item_interactions"

    # Parse users and items into a dictionary each

    print("Parsing Items and Users...")
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))
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

    print("Parsing interacted with users...")
    for itype in range(6):
        for line in open(item_interactions_file + str(itype) + ".csv"):
            newline = line.split()
            item = int(newline[0])
            items[item].interacted_with[itype] = []
            newline = newline[1:]
            for i in newline:
                items[item].interacted_with[itype] += [int(i)]

    print("Building unbuilt interaction lists...")
    for key, value in users.items():
        for i in range(6):
            if i not in users[key].interacted_with:
                users[key].interacted_with[i] = []

    for key, value in items.items():
        for i in range(6):
            if i not in items[key].interacted_with:
                items[key].interacted_with[i] = []

    interactions = parser.parse_interactions(interactions_file, users, items)

    sample = {}
    item_statistics = {}
    for key, i in items.items():
        item_statistics[key] = [0,0, []]

    print("Adding recruited and deleted users to set")
    for key, value in interactions.items():
        if value.interaction_weight() == -1.0 and item_statistics[key[1]][1] < n_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][1] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 4.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 3.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 2.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

        if value.interaction_weight() == 1.0 and item_statistics[key[1]][0] < p_count and key[0] not in item_statistics[key[1]][2]:
            sample[key] = value
            item_statistics[key[1]][0] += 1
            item_statistics[key[1]][2] += [key[0]]

    data_dicts = model.data_dicts()
 
    print("Negative random sampling")
    list_set = list(users.keys())
    for key, value in items.items():
        print(value.interacted_with)
        if not [len(l) for k, l in value.interacted_with.items() if len(l) > 0]:
            continue
        while item_statistics[key][1] < n_count:
            u = random.choice(list_set)
            if u not in item_statistics[key][2] and (u, key) not in sample and not not [len(l) for k, l in users[u].interacted_with.items() if len(l) > 0]:
                sample[(u, key)] = model.Interactions(users[u], items[key], [model.Interaction(4, int(time.time()))], data_dicts)
                item_statistics[key][1] += 1
                item_statistics[key][2] += [u]

    with open("sampled_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in sample.items():
            sort = sorted(value.interactions, key=(lambda x: -x.time))
            writeline = []
            writeline.append(str(key[0]))
            writeline.append(str(key[1]))
            for i in sort:
                writeline.append(str(i.i_type))
                writeline.append(str(i.time))
            csvwriter.writerow(writeline)


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


def training_csv(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)

    with open("label.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, pair in interactions.items():
            print("csv file, outputting user: " + str(pair.user.id) + " item: " + str(pair.item.id))
            clicked = False
            bmR = False
            RI = False
            deleted = False
            for i in pair.interactions:
                if i.i_type == 1 and clicked == False: 
                    clicked = True
                if i.i_type == 2 or i.i_type == 3 and bmR == False: 
                    bmR = True
                if i.i_type == 4 and deleted == False:
                    deleted = True
                if i.i_type == 5 and RI == False:
                    RI = True
            line = []
            line.append(str(pair.item.id))
            line.append(str(pair.user.id))
            if pair.user.premium == 1:
                line.append("prem")
            else:
                line.append("nprem")
            if clicked == True:
                line.append("click")
            else:
                line.append("nclick")
            if bmR == True:
                line.append("reply")
            else:
                line.append("nreply")
            if RI == True:
                line.append("recruit")
            else:
                line.append("nrecruit")
            if deleted == True:
                line.append("delete")
            else:
                line.append("ndelete")
            line.append(str(pair.features()))
            line.append(str(pair.label()))
            csvwriter.writerow(line)


def target_csv(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)
    bst = learner.baseline_learn(users, items, interactions, target_users, target_items, concept_weights)

    with open("target.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        target_i_count = 0
        for item in target_items:
            target_u_count = 0
            if target_i_count > 1000:
                break
            target_i_count += 1
            for user in target_users:
                if target_u_count > 1000:
                    break
                target_u_count += 1
                line = []
                interaction = model.Interactions(users[user], items[item], [])
                test_matrix = xgb.DMatrix(np.array([interaction.features()]))
                pred = bst.predict(test_matrix)

                line.append(str(item))
                line.append(str(user))
                line.append(str(interaction.features()))
                line.append(str(pred))
                csvwriter.writerow(line)

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

def interacted_with(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/sampled_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    item_interactions0 = {}
    item_interactions1 = {}
    item_interactions2 = {}
    item_interactions3 = {}
    item_interactions4 = {}
    item_interactions5 = {}
    user_interactions0 = {}
    user_interactions1 = {}
    user_interactions2 = {}
    user_interactions3 = {}
    user_interactions4 = {}
    user_interactions5 = {}

    for key, value in interactions.items():
        most_recent0 = 0
        most_recent1 = 0
        most_recent2 = 0
        most_recent3 = 0
        most_recent4 = 0
        most_recent5 = 0
        for i in value.interactions:
            if i.i_type == 0 and i.time > most_recent0:
                most_recent0 = i.time
            if i.i_type == 1 and i.time > most_recent1:
                most_recent1 = i.time
            if i.i_type == 2 and i.time > most_recent2:
                most_recent2 = i.time
            if i.i_type == 3 and i.time > most_recent3:
                most_recent3 = i.time
            if i.i_type == 4 and i.time > most_recent4:
                most_recent4 = i.time
            if i.i_type == 5 and i.time > most_recent5:
                most_recent5 = i.time

        for i in value.interactions:
            if i.i_type == 0:
                if key[0] in user_interactions0:
                    user_interactions0[key[0]] += [(key[1], most_recent0)]
                else: 
                    user_interactions0[key[0]] = [(key[1], most_recent0)]
            elif i.i_type == 1:
                if key[0] in user_interactions1:
                    user_interactions1[key[0]] += [(key[1], most_recent1)]
                else: 
                    user_interactions1[key[0]] = [(key[1], most_recent1)]
            elif i.i_type == 2:
                if key[0] in user_interactions2:
                    user_interactions2[key[0]] += [(key[1], most_recent2)]
                else: 
                    user_interactions2[key[0]] = [(key[1], most_recent2)]
            elif i.i_type == 3:
                if key[0] in user_interactions3:
                    user_interactions3[key[0]] += [(key[1], most_recent3)]
                else: 
                    user_interactions3[key[0]] = [(key[1], most_recent3)]
            elif i.i_type == 4:
                if key[0] in user_interactions4:
                    user_interactions4[key[0]] += [(key[1], most_recent4)]
                else: 
                    user_interactions4[key[0]] = [(key[1], most_recent4)]
            elif i.i_type == 5:
                if key[0] in user_interactions5:
                    user_interactions5[key[0]] += [(key[1], most_recent5)]
                else: 
                    user_interactions5[key[0]] = [(key[1], most_recent5)]
 
            if i.i_type == 0:
                if key[1] in item_interactions0:
                    item_interactions0[key[1]] += [(key[0], most_recent0)]
                else: 
                    item_interactions0[key[1]] = [(key[0], most_recent0)]
            elif i.i_type == 1:
                if key[1] in item_interactions1:
                    item_interactions1[key[1]] += [(key[0], most_recent1)]
                else: 
                    item_interactions1[key[1]] = [(key[0], most_recent1)]
            elif i.i_type == 2:
                if key[1] in item_interactions2:
                    item_interactions2[key[1]] += [(key[0], most_recent2)]
                else: 
                    item_interactions2[key[1]] = [(key[0], most_recent2)]
            elif i.i_type == 3:
                if key[1] in item_interactions3:
                    item_interactions3[key[1]] += [(key[0], most_recent3)]
                else: 
                    item_interactions3[key[1]] = [(key[0], most_recent3)]
            elif i.i_type == 4:
                if key[1] in item_interactions4:
                    item_interactions4[key[1]] += [(key[0], most_recent4)]
                else: 
                    item_interactions4[key[1]] = [(key[0], most_recent4)]
            elif i.i_type == 5:
                if key[1] in item_interactions5:
                    item_interactions5[key[1]] += [(key[0], most_recent5)]
                else: 
                    item_interactions5[key[1]] = [(key[0], most_recent5)]

    for key, value in user_interactions0.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions0[key] = [item for item, time in sort]
    for key, value in user_interactions1.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions1[key] = [item for item, time in sort]
    for key, value in user_interactions2.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions2[key] = [item for item, time in sort]
    for key, value in user_interactions3.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions3[key] = [item for item, time in sort]
    for key, value in user_interactions4.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions4[key] = [item for item, time in sort]
    for key, value in user_interactions5.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            user_interactions5[key] = [item for item, time in sort]

    for key, value in item_interactions0.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions0[key] = [item for item, time in sort]
    for key, value in item_interactions1.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions1[key] = [item for item, time in sort]
    for key, value in item_interactions2.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions2[key] = [item for item, time in sort]
    for key, value in item_interactions3.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions3[key] = [item for item, time in sort]
    for key, value in item_interactions4.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions4[key] = [item for item, time in sort]
    for key, value in item_interactions5.items():
            sort = sorted([(item, time) for (item, time) in value], key=(lambda x: -x[1]))
            item_interactions5[key] = [item for item, time in sort]

    with open("user_interactions0.csv", "w") as userf0:
        for key, value in user_interactions0.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf0.write(string)
    with open("user_interactions1.csv", "w") as userf1:
        for key, value in user_interactions1.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf1.write(string)
    with open("user_interactions2.csv", "w") as userf2:
        for key, value in user_interactions2.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf2.write(string)
    with open("user_interactions3.csv", "w") as userf3:
        for key, value in user_interactions3.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf3.write(string)
    with open("user_interactions4.csv", "w") as userf4:
        for key, value in user_interactions4.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf4.write(string)
    with open("user_interactions5.csv", "w") as userf5:
        for key, value in user_interactions5.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf5.write(string)
            
    with open("item_interactions0.csv", "w") as itemf0:
        for key, value in item_interactions0.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf0.write(string)
    with open("item_interactions1.csv", "w") as itemf1:
        for key, value in item_interactions1.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf1.write(string)
    with open("item_interactions2.csv", "w") as itemf2:
        for key, value in item_interactions2.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf2.write(string)
    with open("item_interactions3.csv", "w") as itemf3:
        for key, value in item_interactions3.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf3.write(string)
    with open("item_interactions4.csv", "w") as itemf4:
        for key, value in item_interactions4.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf4.write(string)
    with open("item_interactions5.csv", "w") as itemf5:
        for key, value in item_interactions5.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            itemf5.write(string)

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

def build_visualisations3(directory):
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    user_cold = []
    item_cold = []

    print("Added Users Values")
    for user, value in users.items():
        cold = 0
        l = [value.clevel, value.disc, value.indus, value.country, value.region, value.expn, value.expy, value.expyc, value.edud]
        for i in l:
            if i == 0 or i is None or i == "non_dach":
                cold += 1
        user_cold += [cold]

    print("Added Items Values")
    for item, value in items.items():
        cold = 0
        l = [value.clevel, value.disc, value.indus, value.country, value.region, value.etype,
        value.lat, value.lon]
        for i in l:
            if i == 0 or i is None or i == "non_dach":
                cold += 1
        item_cold += [cold]

    u_stats = Counter(user_cold).most_common(6)
    u_stats.append(("Other", len(users)-sum(row[1] for row in u_stats)))
    i_stats = Counter(item_cold).most_common(6)
    i_stats.append(("Other", len(users)-sum(row[1] for row in i_stats)))

    bargraph_single([k for l, k in u_stats], [l for l, k in u_stats], "Most Common Count of Missing Attributes in Users")
    bargraph_single([k for l, k in i_stats], [l for l, k in i_stats], "Most Common Count of Missing Attributes in Items")


def build_visualisations2(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    user_stats = {"clevel": [], 
                  "disc": [],
                  "indus": [],
                  "country": [],
                  "region": []}

    item_stats = {"disc": [],
                  "indus": [],
                  "clevel": [],
                  "country": [],
                  "region": []}

    interaction_time = []
    interaction_type = []
    interaction_count = []

    print("Added Users Values")
    for user, value in users.items():
        user_stats["clevel"] += [value.clevel]
        user_stats["disc"] += [value.disc]
        user_stats["indus"] += [value.indus]
        user_stats["country"] += [value.country]
        user_stats["region"] += [value.region]

    print("Added Items Values")
    for item, value in items.items():
        item_stats["disc"] += [value.disc]
        item_stats["indus"] += [value.indus]
        item_stats["clevel"] += [value.clevel]
        item_stats["country"] += [value.country]
        item_stats["region"] += [value.region]

    print("Added Interactions Values")
    for key, value in interactions.items():
        interaction_count += [len(value.interactions)]
        for i in value.interactions:
            interaction_type += [i.i_type]
            interaction_time += [i.time]

    u_stats = {}
    i_stats = {}

    for key, value in user_stats.items():
        u_stats[key] = Counter(value)
    for key, value in item_stats.items():
        i_stats[key] = Counter(value)

    interaction_type = Counter(interaction_type)
    interaction_count = Counter(interaction_count)
    
    i_lables = {0: "Impression", 1: "Click", 2: "Bookmark", 3: "Reply/Apply", 4: "Delete", 5: "Recruiter Click"}
    c_lables = {0: "Unknown", 1: "Intern", 2: "Beginner", 3: "Experienced", 4: "Manager", 5: "Executive", 6: "S. Executive"}

    bargraph_single(interaction_type.values(), ([i_lables[x] for x in list(interaction_type.keys())]), "Frequency of Interaction Types")
    bargraph_single(interaction_count.values(), [str(x) for x in list(interaction_count.keys())], "Frequency of Interactions")

    for i in u_stats["clevel"].keys():
        if i_stats["clevel"][i] == 0:
            i_stats["clevel"][i] = 0
    for i in i_stats["clevel"].keys():
        if u_stats["clevel"][i] == 0:
            u_stats["clevel"][i] = 0

    for i in u_stats["country"].keys():
        if i_stats["country"][i] == 0:
            i_stats["country"][i] = 0
    for i in i_stats["country"].keys():
        if u_stats["country"][i] == 0:
            u_stats["country"][i] = 0

    for i in u_stats["region"].keys():
        if i_stats["region"][i] == 0:
            i_stats["region"][i] = 0
    for i in i_stats["region"].keys():
        if u_stats["region"][i] == 0:
            u_stats["region"][i] = 0

    for i in u_stats["indus"].keys():
        if i_stats["indus"][i] == 0:
            i_stats["indus"][i] = 0
    for i in i_stats["indus"].keys():
        if u_stats["indus"][i] == 0:
            u_stats["indus"][i] = 0

    for i in u_stats["disc"].keys():
        if i_stats["disc"][i] == 0:
            i_stats["disc"][i] = 0
    for i in i_stats["disc"].keys():
        if u_stats["disc"][i] == 0:
            u_stats["disc"][i] = 0


    timeseries(interaction_time, "Interaction by Time")
    bargraph_double(u_stats["country"].values(), i_stats["country"].values(), u_stats["country"].keys(), "User Item Country Frequency")
    bargraph_double(u_stats["disc"].values(), i_stats["disc"].values(), u_stats["disc"].keys(), "User Item Discipline Frequency")
    bargraph_double(u_stats["indus"].values(), i_stats["indus"].values(), u_stats["indus"].keys(), "User Item Industry Frequency")
    bargraph_double(u_stats["clevel"].values(), i_stats["clevel"].values(), [c_lables[x] for x in list(u_stats["clevel"].keys())], "User Item Career Level Frequency")
    bargraph_double(u_stats["region"].values(), i_stats["region"].values(), u_stats["region"].keys(), "User Item Region Frequency")


def build_visualisations(directory):
    (users, items, interactions, 
     target_users, target_items) = learner.baseline_parse(directory)

    user_stats = {"clevel": [], 
                  "disc": [],
                  "indus": [],
                  "expn": [],
                  "expy": [],
                  "expyc": [],
                  "edud": [],
                  "country": [],
                  "region": [],
                  "xtcj": [],
                  "jobroles_values": [],
                  "jobroles_count": [],
                  "edufos_values": [],
                  "edufos_count": [],
                  "premium": []} 

    item_stats = {"title_values": [],
                  "title_count": [],
                  "tags_values": [],
                  "tags_count": [],
                  "disc": [],
                  "indus": [],
                  "latlon": [],
                  "clevel": [],
                  "country": [],
                  "region": [],
                  "paid": [],
                  "time": [],
                  "etype": []}
                  
    target_items_intersect = 0
    target_users_intersect = 0
    users_length = len(users)
    items_length = len(items)
    target_items_length = len(target_items)
    target_users_length = len(target_users)
    target_items_not_in_set = 0
    target_users_not_in_set = 0
    interaction_time = []
    interaction_type = []
    interaction_count = []
    target_users_interactions = set()
    target_items_interactions = set()
    user_interactions = set()
    item_interactions = set()
    
    for user, value in users.items():
        for c in value.jobroles:
            user_stats["jobroles_values"] += [c]
        user_stats["jobroles_count"] += [len(value.jobroles)]
        for c in value.edufos:
            user_stats["edufos_values"] += [c]
        user_stats["edufos_count"] += [len(value.edufos)]
        user_stats["clevel"] += [value.clevel]
        user_stats["disc"] += [value.disc]
        user_stats["indus"] += [value.indus]
        user_stats["expn"] += [value.expn]
        user_stats["expy"] += [value.expy]
        user_stats["expyc"] += [value.expyc]
        user_stats["edud"] += [value.edud]
        user_stats["country"] += [value.country]
        user_stats["region"] += [value.region]
        user_stats["xtcj"] += [value.xtcj]
        user_stats["premium"] += [value.premium]
        if user in target_users:
            target_users_intersect += 1

    for u in target_users:
        if u not in users:
            target_users_not_in_set += 1

    for item, value in items.items():
        for c in value.title:
            item_stats["title_values"] += [c]
        item_stats["title_count"] += [len(value.title)]
        for c in value.tags:
            item_stats["tags_values"] += [c]
        item_stats["tags_count"] += [len(value.tags)]
        item_stats["disc"] += [value.disc]
        item_stats["indus"] += [value.indus]
        item_stats["clevel"] += [value.clevel]
        item_stats["country"] += [value.country]
        item_stats["region"] += [value.region]
        item_stats["paid"] += [value.paid]
        item_stats["etype"] += [value.etype]
        item_stats["time"] += [value.time]
        item_stats["latlon"] += [(value.lat, value.lon)]
        if item in target_items:
            target_items_intersect += 1

    for i in target_items:
        if i not in items:
            target_items_not_in_set += 1

    for key, value in interactions.items():
        interaction_count += [len(value.interactions)]
        for i in value.interactions:
            interaction_type += [i.i_type]
            interaction_time += [i.time]
        if value.user.id in target_users:
            target_users_interactions.add(value.user.id)
        if value.item.id in target_items:
            target_items_interactions.add(value.item.id)
        if value.item.id in items:
            item_interactions.add(value.item.id)
        if value.user.id in users:
            user_interactions.add(value.user.id)

    for key, value in user_stats.items():
        user_stats[key] = Counter(value)
    for key, value in item_stats.items():
        item_stats[key] = Counter(value)

    interaction_type = Counter(interaction_type)
    interaction_count = Counter(interaction_count)
    target_users_interactions = len(target_users_interactions)
    target_items_interactions = len(target_items_interactions)
    user_interactions = len(user_interactions)
    item_interactions = len(item_interactions)
    
    i_lables = {0: "Impression", 1: "Click", 2: "Bookmark", 3: "Reply/Apply", 4: "Delete", 5: "Recruiter Click"}
    c_lables = {0: "Unknown", 1: "Intern", 2: "Beginner", 3: "Experienced", 4: "Manager", 5: "Executive", 6: "S. Executive"}

    bargraph_single(interaction_type.values(), ([i_lables[x] for x in list(interaction_type.keys())]), "Frequency of Interaction Types")
    bargraph_single(interaction_count.values(), [str(x) for x in list(interaction_count.keys())], "Frequency of Interactions")

    for i in user_stats["clevel"].keys():
        if item_stats["clevel"][i] == 0:
            item_stats["clevel"][i] = 0
    for i in item_stats["clevel"].keys():
        if user_stats["clevel"][i] == 0:
            user_stats["clevel"][i] = 0

    for i in user_stats["country"].keys():
        if item_stats["country"][i] == 0:
            item_stats["country"][i] = 0
    for i in item_stats["country"].keys():
        if user_stats["country"][i] == 0:
            user_stats["country"][i] = 0

    for i in user_stats["region"].keys():
        if item_stats["region"][i] == 0:
            item_stats["region"][i] = 0
    for i in item_stats["region"].keys():
        if user_stats["region"][i] == 0:
            user_stats["region"][i] = 0

    for i in user_stats["indus"].keys():
        if item_stats["indus"][i] == 0:
            item_stats["indus"][i] = 0
    for i in item_stats["indus"].keys():
        if user_stats["indus"][i] == 0:
            user_stats["indus"][i] = 0

    for i in user_stats["disc"].keys():
        if item_stats["disc"][i] == 0:
            item_stats["disc"][i] = 0
    for i in item_stats["disc"].keys():
        if user_stats["disc"][i] == 0:
            user_stats["disc"][i] = 0


    timeseries(interaction_time, "Interaction by Time")

    bargraph_double(user_stats["country"].values(), item_stats["country"].values(), user_stats["country"].keys(), "User Item Country Frequency")
    bargraph_double(user_stats["disc"].values(), item_stats["disc"].values(), user_stats["disc"].keys(), "User Item Discipline Frequency")
    bargraph_double(user_stats["indus"].values(), item_stats["indus"].values(), user_stats["indus"].keys(), "User Item Industry Frequency")
    bargraph_double(user_stats["clevel"].values(), item_stats["clevel"].values(), [c_lables[x] for x in list(user_stats["clevel"].keys())], "User Item Career Level Frequency")
    bargraph_double(user_stats["region"].values(), item_stats["region"].values(), user_stats["region"].keys(), "User Item Region Frequency")

    with open("somestats.txt", "w") as f:
        for key, value in user_stats.items():
            f.write("user " + key + str(user_stats[key]) + "\n")
        for key, value in item_stats.items():
            f.write("item " + key + str(item_stats[key]) + "\n")
        f.write("uniquejobroles"+str(len(user_stats["jobroles_values"])) + "\n")
        f.write("uniquetitle"+str(len(item_stats["title_values"])) + "\n")
        f.write("uniquetags"+str(len(item_stats["tags_values"])) + "\n")
        f.write("jobrolescount"+str(user_stats["jobroles_count"]) + "\n")
        f.write("titlecount"+str(item_stats["title_count"]) + "\n")
        f.write("tagscount"+str(item_stats["tags_count"]) + "\n")
        f.write("targetuserinteractions"+str(target_users_interactions) + "\n")
        f.write("targetiteminteractions"+str(target_items_interactions) + "\n")
        f.write("userinteractions"+str(user_interactions) + "\n")
        f.write("iteminteractions"+str(item_interactions) + "\n")
        f.write("targetitemsinterset"+str(target_items_intersect) + "\n")
        f.write("targetuserintersect"+str(target_users_intersect) + "\n")
        f.write("userlength"+str(users_length) + "\n")
        f.write("itemlength"+str(items_length) + "\n")
        f.write("targetitemlength"+str(target_items_length) + "\n")
        f.write("targetuserlength"+str(target_users_length) + "\n")
        f.write("targetitemsnotinuset"+str(target_items_not_in_set) + "\n")
        f.write("targetusersnotinset"+str(target_users_not_in_set) + "\n")

def timeseries(values, title):
    n, bins = np.histogram(values, 50)
    bincenters = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bincenters,n,'-')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(title)

def pigraph(values, labels, title):
    m = max(enumerate(values), key=lambda x: x[1])[0]
    explode = [0]*len(values)
    explode[m] = 0.1

    fig1, ax1 = plt.subplots()
    ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)

    plt.tight_layout()
    plt.savefig(title)

def bargraph_double(values1, values2, labels, title):
    ind = np.arange(len(labels))
    width = 1/(len(labels))
    fix, ax = plt.subplots()

    if len(labels) > 12:
        width = 0.3
        fig, ax = plt.subplots(figsize=(12.5, 4.75))

    rects1 = ax.bar(ind, values1, width, color='b')
    rects2 = ax.bar(ind+width, values2, width, color='r')

    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.set_xticks(ind + (width-0.03)/2)
    ax.set_xticklabels(labels)

    ax.legend((rects1[0], rects2[0]), ('Users', 'Items'))

    """
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.00*height,
                    '%d' % int(height),
                    ha='center', va='bottom')



    if len(labels) < 12:
        autolabel(rects1)
        autolabel(rects2)
    """

    plt.tight_layout()
    plt.savefig(title)

def bargraph_single(values, labels, title):
    ind = np.arange(len(values))
    width = 3/len(values)

    fix, ax = plt.subplots()
    rects = ax.bar(ind, values, width, color='b')

    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.00*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects)

    plt.tight_layout()
    plt.savefig(title)

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
