"""
Baseline solution for the ACM Recsys Challenge 2017
using XGBoost

by Daniel Kohlsdorf
"""

from baseline import parser
from baseline import model
from baseline import predict_worker

import time
import multiprocessing
import pathlib
import xgboost as xgb
import numpy as np

def baseline_parse(data_directory):
    print(" --- Recsys Challenge 2017 Baseline --- ")

    # Set directory strings
    users_file = data_directory + "/mode_users.csv"
    items_file = data_directory + "/mode_items.csv"
    target_users_file = data_directory + "/targetUsers.csv"
    target_items_file = data_directory + "/sampled_targetItems.csv"
    interactions_file = data_directory + "/sampled_interactions.csv"
    user_interactions_file = data_directory + "/user_interactions"
    item_interactions_file = data_directory + "/item_interactions"
    #item_concept_weights_file = data_directory + "/item_concept_weights.csv"
    #user_concept_weights_file = data_directory + "/user_concept_weights.csv"
    #item_concept_interactions_file = data_directory + "/item_concept_interactions.csv"
    #user_concept_interactions_file = data_directory + "/user_concept_interactions.csv"

    parsing_time = time.time()

    print("Parsing Items and Users...")

    # Parse users and items into a dictionary each
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
    """
    # frequency of concepts
    item_concept_weights = {}
    print("Parsing item concept weights...")
    for line in open(item_concept_weights_file):
        newline = line.split() 
        item_concept_weights[int(newline[0])] = int(newline[1])

    # frequency of concepts
    user_concept_weights = {}
    print("Parsing user concept weights...")
    for line in open(user_concept_weights_file):
        newline = line.split() 
        user_concept_weights[int(newline[0])] = int(newline[1])

    # CBF built concepts
    count = 0
    for line in open(item_concept_interactions_file):
        count = count + 1
        if count % 100000 == 0:
            print("... reading line " + str(count) + " from file " + item_concept_interactions_file)
        newline = line.split()
        for i in range(1, len(newline), 2):
            items[int(newline[0])].CBF_weights[int(newline[i])] = int(newline[i+1])

    # CBF built concepts
    count = 0
    for line in open(user_concept_interactions_file):
        count = count + 1
        if count % 100000 == 0:
            print("... reading line " + str(count) + " from file " + user_concept_interactions_file)
        newline = line.split()
        for i in range(1, len(newline), 2):
            users[int(newline[0])].CBF_weights[int(newline[i])] = int(newline[i+1])
    """
    
    print("Parsing Interactions")
    interactions = parser.parse_interactions(interactions_file, users, items)

    # Build target users as a set ignoring user_id line in the csv file
    target_users = []
    print("Parsing target users...")
    for line in open(target_users_file):
        newline = line.strip()
        target_users += [int(newline)]
    target_users = set(target_users)

    # Build target items as a list
    target_items = []
    print("Parsing target items...")
    for line in open(target_items_file):
        target_items += [int(line.strip())]

    z = time.time() - parsing_time
    print("time it took to parse: " + str(z))

    # Return all 5 datasets
    return (users, items, interactions, target_users, target_items)


def matrix_worker(target, items, fname):
    with open(fname, "w") as f:
        for key in target.keys():
            f.write(str(target[key].label()) + " " + " ".join([str(a) + ":" + str(b) for (a, b) in enumerate(target[key].features(items)) if b != 0]) + "\n")

def baseline_learn(users, items, interactions, target_users, target_items):
    n_workers = 47
    pathlib.Path('temp').mkdir(parents=True, exist_ok=True) 

    a = time.time()

    print("Running matrix workers")
    # Schedule classification
    bucket_size = (len(interactions) / n_workers) + 1
    start = 0
    jobs = []
    for i in range(0, n_workers):
        stop = int(min(len(interactions), start + bucket_size))
        filename = "temp/matrix_" + str(i) + ".csv"
        process = multiprocessing.Process(target = matrix_worker,
                                            args = (dict(list(interactions.items())[start:stop]),
                                            items, filename))
        jobs.append(process)
        start = stop

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    z = time.time() - a
    print("time it took to build features for interaction: " + str(z))

    print("Combining Matrix workers")
    result_file = open("temp/datamatrix.txt.train", "w") 
    for i in range(0, n_workers):
        filename = "temp/matrix_" + str(i) + ".csv"
        tempfile = open(filename, "r")
        result_file.write(tempfile.read())
    result_file.close()

    # Build recsys training data
    a = time.time()

    print("Building data matrix...")
    dtrain = xgb.DMatrix("temp/datamatrix.txt.train")
    z = time.time() - a
    print("time it took to parse and build datamatrix: " + str(z))

    # Train XGBoost regression model with maximum tree depth of 6 and 50 trees
    print("Building xgboost tree...")
    evallist = [(dtrain, "train")]
    param = {"bst:max_depth": 15, "bst:eta": 0.1, "bst:colsample_bytree": 0.6, "silent": 1, "objective": "binary:logistic"}
    param["nthread"] = 47
    param["eval_metric"] = "auc"
    param["base_score"] = 0.1
    num_round = 500

    bst = xgb.train(param, dtrain, num_round, evallist)

    return bst


def baseline_predict(users, items, target_users, target_items, bst, result_name):
    n_workers = 47

    pathlib.Path('temp').mkdir(parents=True, exist_ok=True) 
    
    # Schedule classification
    bucket_size = (len(target_items) / n_workers) + 1
    start = 0
    jobs = []
    for i in range(0, n_workers):
        stop = int(min(len(target_items), start + bucket_size))
        filename = "temp/solution_" + str(i) + ".csv"
        process = multiprocessing.Process(target = predict_worker.worker,
                                          args=(target_items[start:stop],
                                            target_users, items,
                                            users, filename, bst))
        jobs.append(process)
        start = stop

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    pathlib.Path('solution').mkdir(parents=True, exist_ok=True) 
    result_file = open("solution/" + result_name, "w") 
    for i in range(0, n_workers):
        filename = "temp/solution_" + str(i) + ".csv"
        tempfile = open(filename, "r")
        result_file.write(tempfile.read())

