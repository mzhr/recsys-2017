"""
Baseline solution for the ACM Recsys Challenge 2017
using XGBoost

by Daniel Kohlsdorf
"""


from baseline import parser
from baseline import predict_worker

import multiprocessing
import pathlib
import xgboost as xgb
import numpy as np


def baseline_parse(data_directory):
    print(" --- Recsys Challenge 2017 Baseline --- ")

    # Set directory strings
    users_file = data_directory + "/users.csv"
    items_file = data_directory + "/items.csv"
    target_users_file = data_directory + "/targetUsers.csv"
    target_items_file = data_directory + "/targetItems.csv"
    # Minified interactions
    interactions_file = data_directory + "/minified_interactions.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = parser.select(users_file, lambda x: True, parser.build_user, lambda x: int(x[0]))
    (header_items, items) = parser.select(items_file, lambda x: True, parser.build_item, lambda x: int(x[0]))

    interactions = parser.parse_interactions(interactions_file, users, items)

    # Build target users as a set ignoring user_id line in the csv file
    target_users = []
    for line in open(target_users_file):
        newline = line.strip()
        target_users += [int(newline)]
    target_users = set(target_users)

    # Build target items as a list
    target_items = []
    for line in open(target_items_file):
        target_items += [int(line.strip())]

    # Return all 5 datasets
    return (users, items, interactions, target_users, target_items)


def baseline_learn(users, items, interactions, target_users, target_items):
    # Build recsys training data
    data = np.array([interactions[key].features() for key in interactions.keys()])
    labels = np.array([interactions[key].label() for key in interactions.keys()])
    dataset = xgb.DMatrix(data, label=labels)
    #dataset.save_binary("recsys2017.buffer")

    # Train XGBoost regression model with maximum tree depth of 6 and 50 trees
    evallist = [(dataset, "train")]
    param = {"bst:max_depth": 2, "bst:eta": 0.1, "silent": 1, "objective": "reg:linear"}
    param["nthread"] = 47
    param["eval_metric"] = "rmse"
    param["base_score"] = 0.0
    num_round = 25
    bst = xgb.train(param, dataset, num_round, evallist)
    #bst.save_model("recsys2017.model")
    #bst = xgb.Booster()
    #bst.load_model("recsys2017.model")

    return bst


def baseline_predict(users, items, target_users, target_items, bst, result_name):
    n_workers = 47

    pathlib.Path('temp').mkdir(parents=True, exist_ok=True) 

    # Schedule classification
    bucket_size = len(target_items) / n_workers
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
        result_file.write(tempfile.read() + "\n")
