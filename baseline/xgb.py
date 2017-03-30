"""
Baseline solution for the ACM Recsys Challenge 2017
using XGBoost

by Daniel Kohlsdorf
"""

import multiprocessing
import random
import argparse
import xgboost as xgb
import numpy as np

from baseline.parser import select, build_user, build_item, InteractionBuilder
from baseline.recommendation_worker import classify_worker

def baseline_learn(data_directory):
    """
    Takes in directory of data and target items to generate recommendations.
    """
    print(" --- Recsys Challenge 2017 Baseline --- ")

    N_WORKERS         = 47
    USERS_FILE        = data_directory + "/users.csv"
    ITEMS_FILE        = data_directory + "/items.csv"
    INTERACTIONS_FILE = data_directory + "/interactions.csv"
    TARGET_USERS      = data_directory + "/targetUsers.csv"
    TARGET_ITEMS      = data_directory + "/targetItems.csv"


    """
    1) Parse the challenge data, exclude all impressions
       Exclude all impressions
    """
    (header_users, users) = select(USERS_FILE, lambda x: True, build_user, lambda x: int(x[0]))
    (header_items, items) = select(ITEMS_FILE, lambda x: True, build_item, lambda x: int(x[0]))

    builder = InteractionBuilder(users, items)
    (header_interactions, interactions) = select(
        INTERACTIONS_FILE,
        lambda x: x[2] != "0",
        builder.build_interaction,
        lambda x: (int(x[0]), int(x[1]))
    )


    """
    2) Build recsys training data
    """
    data = np.array([interactions[key].features() for key in interactions.keys()])
    labels = np.array([interactions[key].label() for key in interactions.keys()])
    dataset = xgb.DMatrix(data, label=labels)
    dataset.save_binary("recsys2017.buffer")


    """
    3) Train XGBoost regression model with maximum tree depth of 6 and 50 trees
    """
    evallist = [(dataset, "train")]
    param = {"bst:max_depth": 2, "bst:eta": 0.1, "silent": 1, "objective": "reg:linear"}
    param["nthread"] = 47
    param["eval_metric"] = "rmse"
    param["base_score"] = 0.0
    num_round = 30
    bst = xgb.train(param, dataset, num_round, evallist)
    bst.save_model("recsys2017.model")


    """
    4) Create target sets for items and users
    """
    target_users = []
    for line in open(TARGET_USERS):
        newline = line.strip()
        if newline != "user_id":
            target_users += [int(newline)]
    target_users = set(target_users)

    target_items = []
    for line in open(TARGET_ITEMS):
        target_items += [int(line.strip())]


    """
    5) Schedule classification
    """
    bucket_size = len(target_items) / N_WORKERS
    start = 0
    jobs = []
    for i in range(0, N_WORKERS):
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
