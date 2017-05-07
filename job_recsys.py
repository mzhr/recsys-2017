#!/usr/bin/env python3

"""
MAZHAR STUFF
"""

import argparse
from time import gmtime, time
from baseline import xgb

def run():
    """
    Gets Directory from commandline options and starts the xgboost 
    baseline learning algorithm.
    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("data_directory",
        help="""Location of User.csv, Items.csv, Interactions.csv,
                TargetItems.csv and TargetUsers.csv""")
    args = parser.parse_args()

    result_name = "submit" + str(time())[:10] + ".csv"
    (users, items, 
     interactions, 
     target_users, 
     target_items) = xgb.baseline_parse(args.data_directory)
    xgb.baseline_learn(users, items, interactions, target_users, target_items, result_name)


def cross_validation(interactions, fold):
    """
    Fold Cross validation of the learning model
    """

    # Fold must be between 0 and 10
    assert fold > 0 and fold < 10

    # Times of interactions from first time to final event evem distribution
    fold_splits = [1478392842, 
                   1478981224, 
                   1479386595,
                   1483518634,
                   1483961181,
                   1484302454,
                   1484648610,
                   1485179035,
                   1485384558,
                   1485845069,
                   1486506722]
    time = gmtime(fold_splits[fold])

    (users, items, data_interactions, target_interactions, target_users, target_items) = build_validation_data(interactions, time)
    result_name = "test" + str(fold) + str(time())[:10] + ".csv"
    xgb.baseline_learn(users, items,
                       data_interactions, 
                       target_users, target_items, result_name)
    calculate_score(result_name, target_interactions)


def build_validation_data(interactions, time):
    # Split target users and interactions based on that,
    target_interactions = {}
    data_interactions = {}
    users = {} 
    items = {} 
    target_users = []
    target_items = []

    def add_interaction(data, key, value):
        if key in data:
            data[key].interactions.append(i)
        else:
            data[key] = value

    for key, value in interactions.items():
        for i in value.interactions:
            if i.time > time: 
                target_items.append(value.item.id)
                target_users.append(value.user.id)
                add_interaction(target_interactions, key, i)
            else:
                users[value.user.id] = value.user
                items[value.item.id] = value.item
                add_interaction(data_interactions, key, i)
    return (users, items, data_interactions, target_interactions, target_users, target_items)


def calculate_score(result_name, target_interactions):
    # Calculate Score
    total_score = 0
    for line in open(result_name):
        # Parse line into id's wiht suers as sets for quick compare
        result = line.strip().split("\t")
        item = int(result[0])
        recommendations = result[1].split(", ")
        for user in recommendations:
            user = int(recommendations)

        item_score = 0
        event_score = 0
        premium = 0
        paid = 0




if __name__ == "__main__":
    run()
