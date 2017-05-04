"""
Baseline solution for the ACM Recsys Challenge 2017
using XGBoost

by Daniel Kohlsdorf
"""

import multiprocessing
import xgboost as xgb
import numpy as np

from baseline.parser import select, build_user, build_item, InteractionBuilder
from baseline.recommendation_worker import classify_worker

def baseline_parse(data_directory):
    """
    Takes in directory of data and target items to generate recommendations.
    Parses users, items, interactions, and target items and users.
    """
    print(" --- Recsys Challenge 2017 Baseline --- ")

    # Set directory strings
    users_file = data_directory + "/users.csv"
    items_file = data_directory + "/items.csv"
    interactions_file = data_directory + "/interactions.csv"
    target_users_file = data_directory + "/targetUsers.csv"
    target_items_file = data_directory + "/targetItems.csv"

    # Parse users and items into a dictionary each
    (header_users, users) = select(users_file, lambda x: True, build_user, lambda x: int(x[0]))
    (header_items, items) = select(items_file, lambda x: True, build_item, lambda x: int(x[0]))

    # Build users containing the class of the item and user of the interactions
    builder = InteractionBuilder(users, items)
    (header_interactions, interactions) = select(
        interactions_file,
        lambda x: x[2] != "0",
        #lambda x: True,
        builder.build_interaction,
        lambda x: (int(x[0]), int(x[1]))
    )
    
    interactions = builder.user_item_pair

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


def baseline_learn(users, items, interactions, target_users, target_items, result_name):
    """
    Processes and learns data set againts features to make list of ranked
    recommendations.
    """

    n_workers = 47

    # Build recsys training data
    data = np.array([interactions[key].features() for key in interactions.keys()])
    labels = np.array([interactions[key].label() for key in interactions.keys()])
    dataset = xgb.DMatrix(data, label=labels)
    dataset.save_binary("recsys2017.buffer")

    # Train XGBoost regression model with maximum tree depth of 6 and 50 trees
    evallist = [(dataset, "train")]
    param = {"bst:max_depth": 2, "bst:eta": 0.1, "silent": 1, "objective": "reg:linear"}
    param["nthread"] = 47
    param["eval_metric"] = "rmse"
    param["base_score"] = 0.0
    num_round = 50
    bst = xgb.train(param, dataset, num_round, evallist)
    bst.save_model("recsys2017.model")

    # Schedule classification
    bucket_size = len(target_items) / n_workers
    start = 0
    jobs = []
    for i in range(0, n_workers):
        stop = int(min(len(target_items), start + bucket_size))
        filename = "solution_" + str(i) + ".csv"
        process = multiprocessing.Process(target = classify_worker,
                                          args=(target_items[start:stop],
                                            target_users, items,
                                            users, filename, bst))
        jobs.append(process)
        start = stop

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    result_file = open(result_name, "w") 
    for i in range(0, n_workers):
        filename = "solution_" + str(i) + ".csv"
        tempfile = open(filename, "r")
        result_file.write(tempfile.read() + "\n")
