from baseline import learner, model, parser 

import csv
import random
import time
from collections import Counter
import xgboost as xgb
import numpy as np

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

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))
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
 
    print("Negative random sampling")
    list_set = list(users.keys())
    for key, value in items.items():
        while item_statistics[key][1] < n_count:
            u = random.choice(list_set)
            if u not in item_statistics[key][2] and (u, key) not in sample:
                sample[(u, key)] = model.Interactions(users[u], items[key], [model.Interaction(4, int(time.time()))])
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


def build_cache(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items) = learner.baseline_parse(directory)

    with open("target.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_NONE)
        dicts = model.data_dicts() 
        for user, u in users.items():
            for item, i in items.items():
                line = []
                interaction = model.Interactions(u, i, [], dicts)
                line.append(user)
                line.append(item)
                line.append(','.join(str(a) for a in interaction.features()))
                csvwriter.writerow(line)

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

##KJASDNSAKJNDSAKJDNKJASD
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
    interaction_type = []
    interaction_count = []
    target_user_interactions = set()
    target_item_interactions = set()
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
            target_user_intersect += 1

    for u in target_users:
        if u not in users:
            target_users_not_in_set += 1

    for item, value in items.items():
        for c in value.title:
            item_stats["title_values"] += [c]
        item_stats["title_count"] += [len(value.title)]
        for c in value.tags:
            item_stats["tags_values"] += [c]
        user_stats["tags_count"] += [len(value.tags)]
        item_stats["disc"] += [value.disc]
        item_stats["indus"] += [value.indus]
        item_stats["clevel"] += [value.clevel]
        item_stats["country"] += [value.country]
        item_stats["region"] += [value.region]
        item_stats["paid"] += [value.paid]
        item_stats["etype"] += [value.etype]
        item_stats["time"] += [value.time]
        item_stats["latlon"] += [(value.lat, value.lon)]
        if item in target_item:
            target_item_intersect += 1

    for i in target_items:
        if i not in items:
            target_items_not_in_set += 1

    for key, value in interactions.items():
        interaction_count += [len(value.interactions)]
        for i in value.interactions:
            interaction_type += [i.i_type]
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
    interaction_count = Counter(interaction_count)
    target_user_interactions = len(target_user_interactions)
    target_item_interactions = len(target_item_interactions)
    user_interactions = len(user_interactions)
    item_interactions = len(item_interactions)
