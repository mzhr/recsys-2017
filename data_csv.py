from baseline import learner, model, parser 

import csv
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
            if (newline[0], newline[1]) not in interactions:
                interactions[(newline[0], newline[1])] = [(newline[2], newline[3])]
            else:
                interactions[(newline[0], newline[1])].append(
                        (newline[2], newline[3])) 

    with open("minified_interactions.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in interactions.items():
            sort = sorted([(item, value) for (item, time) in value], key=(lambda x: -x[1]))
            writeline = []
            writeline.append(key[0])
            writeline.append(key[1])
            for i in sort:
                writeline.append(i[0])
                writeline.append(i[1])
            csvwriter.writerow(writeline)

def concept_statistics(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)

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

    with open("concept_weights.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for key, value in concept_stats.items():
            writeline = []
            writeline.append(str(key))
            writeline.append(str(value))
            csvwriter.writerow(writeline)

def user_concept_statistics(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)

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
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)

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
    (users, items, 
     interactions, 
     target_users, 
     target_items,
     concept_weights) = learner.baseline_parse(directory)

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

def interacted_with(directory):
    # Set directory strings
    users_file = directory + "/users.csv"
    items_file = directory + "/items.csv"
    interactions_file = directory + "/minified_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    item_interactions = {}
    user_interactions = {}

    for key, value in interactions.items():
        most_recent = 0
        for i in value.interactions:
            if i.time > most_recent:
                most_recent = i.time

        if key[0] in user_interactions:
            user_interactions[key[0]].add((key[1], time))
        else: 
            user_interactions[key[0]] = set(([key[1]], time))

        if key[1] in item_interactions:
            item_interactions[key[1]].add((key[0], time))
        else: 
            item_interactions[key[1]] = set(([key[0]], time))

    for key, value in item_interactions.items():
        sort = sorted([item for item, time in value], key=(lambda x: -x[1]))
        item_interactions[key] = [item for item, time in sort]

    for key, value in user_interactions.items():
        sort = sorted([item for item, time in value], key=(lambda x: -x[1]))
        user_interactions[key] = [item for item, time in sort]
       
    with open("user_interactions.csv", "w") as userf:
        for key, value in user_interactions.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf.write(string)
            
    with open("item_interactions.csv", "w") as userf:
        for key, value in item_interactions.items():
            string = str(key)
            for v in value:
                string += " " + str(v)
            string += "\n"
            userf.write(string)


def onehotmodel_generater(directory):
    user_attr = {"clevel": [0,1,2,3,4,5,6],
        "disc":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "indus":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "expn": [0,1,2,3],
        "expy": [0,1,2,3,4,5,6],
        "expyc": [0,1,2,3,4,5,6],
        "edud": [0,1,2,3],
        "country": ['"de"','"at"','"ch"','"non dach"'],
        "region": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
        "xtcj": [0,1]}

    user_array_attr = {
        "edufos": [1,2,3,4,5,6,7,8,9],
        "jobroles": []}

    item_attr = {"clevel": [0,1,2,3,4,5,6],
        "disc":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "indus":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
        "country": ['"de"','"at"','"ch"','"non dach"'],
        "region": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
        "paid": [0,1],
        "etype":[1,2,3,4],
        "lat": [52.5,48.2,None,53.6,50.1,47.4,48.8,50.9,51.2,48.1,51.5,49.5,52.4,51.1,51.4,
                49.0,48.7,51.3,50.8,47.6,50.0,48.4,51.0,53.5,53.1,52.3,50.7,48.0,52.0,47.2,47.1,
                48.3,47.8,46.9,48.9,47.5,47.7,49.9,48.5,47.0,49.2,50.6,49.8,47.3,49.4,52.1,51.7,
                49.1,52.2,48.6,51.6,47.9,51.8,49.3,50.2,50.4,49.6,53.7,51.9,54.3,50.3,53.9,54.1,
                53.2,49.7,46.8,53.8,52.6,53.3,53.4,50.5,53.0,52.7,46.6,52.8,52.9,46.2,54.8,54.2,
                46.7,46.5,54.5,54.0,54.4,46.3],
        "lon": [13.4,11.6,None,8.7,10.0,8.5,9.2,7.0,6.8,9.7,8.8,8.4,7.6,8.6,8.3,16.4,7.2,11.1,7.5,
                13.1,7.1,12.4,7.9,7.4,9.5,10.1,11.0,9.9,11.4,12.1,8.2,8.1,9.1,13.8,8.9,7.3,10.9,9.0,9.3,
                9.4,10.2,7.8,9.8,8.0,10.3,10.5,11.7,6.9,13.0,9.6,10.8,6.1,6.6,10.7,12.9,14.3,13.7,12.2,
                7.7,11.5,11.3,12.0,11.9,10.4,6.7,11.8,10.6,12.5,16.2,12.6,13.3,11.2,16.3,13.5,12.8,6.4,
                15.4,12.3,12.7,13.9,14.0,14.6,13.6,13.2,6.5,14.4,15.6,6.3,14.2,6.2,15.5,14.1,14.5,15.0,
                15.7,15.3]}

    item_array_attr = {
        "title": [],
        "tags": []}

    for line in open(directory + "/item_concept_weights.csv"):
        newline = line.split() 
        if int(newline[1]) > 500: 
            user_array_attr["jobroles"] += [int(newline[0])]

    # frequency of concepts
    for line in open(directory + "/user_concept_weights.csv"):
        newline = line.split() 
        if int(newline[1]) > 500: 
            item_array_attr["title"] += [int(newline[0])]
            item_array_attr["tags"] += [int(newline[0])]

    feature_count = 0
    with open("onehotmodel.txt", "w") as f:
        for key, values in user_attr.items():
            count = 0
            for attr in values:
                f.write("\tdef user_" + str(key) + str(count) + "(self):\n")
                f.write("\t\tif self.user." + str(key) + " == " + str(attr) + ":\n")
                f.write("\t\t\treturn 1.0\n")
                f.write("\t\telse:\n")
                f.write("\t\t\treturn 0.0\n\n")
                count += 1
                feature_count +=1

        for key, values in user_array_attr.items():
            for attr in values:
                f.write("\tdef user_" + str(key) + str(attr) + "(self):\n")
                f.write("\t\tif " + str(attr) + " in self.user." + str(key) + ":\n")
                f.write("\t\t\treturn 1.0\n")
                f.write("\t\telse:\n")
                f.write("\t\t\treturn 0.0\n\n")
                feature_count +=1
        
        for key, values in item_attr.items():
            count = 0
            for attr in values:
                f.write("\tdef item_" + str(key) + str(count) + "(self):\n")
                f.write("\t\tif self.item." + str(key) + " == " + str(attr) + ":\n")
                f.write("\t\t\treturn 1.0\n")
                f.write("\t\telse:\n")
                f.write("\t\t\treturn 0.0\n\n")
                count += 1
                feature_count +=1

        for key, values in item_array_attr.items():
            for attr in values:
                f.write("\tdef user_" + str(key) + str(attr) + "(self):\n")
                f.write("\t\tif self.item." + str(key) + " == " + str(attr) + ":\n")
                f.write("\t\t\treturn 1.0\n")
                f.write("\t\telse:\n")
                f.write("\t\t\treturn 0.0\n\n")
                feature_count +=1

        for key, values in user_attr.items():
            count = 0
            for attr in values:
                f.write("\t\t\tself.user_" + str(key) + str(count) + "(),\n")
                count += 1

        for key, values in user_array_attr.items():
            for attr in values:
                f.write("\t\t\tself.user_" + str(key) + str(attr) + "(),\n")

        for key, values in item_attr.items():
            count = 0
            for attr in values:
                f.write("\t\t\tself.item_" + str(key) + str(count) + "(),\n")
                count += 1

        for key, values in item_array_attr.items():
            for attr in values:
                f.write("\t\t\tself.user_" + str(key) + str(attr) + "(),\n")

        print(feature_count)

def build_visualisations(directory):
    (users, items, interactions, 
     target_users, target_items, 
     user_cw, item_cw) = learner.baseline_parse(directory)


