from baseline import learner, model 

import csv
import xgboost as xgb
import numpy as np

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
        csvwriter = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in interactions.items():
            writeline = []
            writeline.append((newline[0], newline[1]))
            for i in value:
                writeline.append(i[0])
                writeline.append(i[1])
            csvwriter.writerow(writeline)

def concept_statistics(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items) = learner.baseline_parse(directory)

    concept_stats = {}
    for item in items.items()
        for c in item.tags:
            if c in concept_stats:
                concept_stats[c] = concept_stats[c] + 1
            else:
                concept_stats[c] = 1
        for c in item.title:
            if c in concept_stats:
                concept_stats[c] = concept_stats[c] + 1
            else:
                concept_stats[c] = 1

    with open("concept_weights.csv", "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in concept_stats.items():
            writeline = []
            writeline.append(key)
            writeline.append(value)
            csvwriter.writerow(writeline)


def training_csv(directory):
    (users, items, 
     interactions, 
     target_users, 
     target_items) = learner.baseline_parse(directory)

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
     target_items) = learner.baseline_parse(directory)
    bst = learner.baseline_learn(users, items, interactions, target_users, target_items)

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
