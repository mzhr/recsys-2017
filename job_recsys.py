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

"""
def cross_validation(interactions, fold):
    Fold Cross validation of the learning model

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

    # Split target users and itneractions based on that,
    target_interactions = {}
    data_interactions = {}
    users = {} 
    items = {} 
    target_users = []
    target_items = []

    for key, value in interactions.items():
        if interactions.time > time: 
            target_items.append(value.item.id)
            target_users.append(value.user.id)
            target_interactions[key] = value
        else:
            users[value.user.id] = value.user
            items[value.item.id] = value.item
            data_interactions[key] = value

    result_name = "test" + str(fold) + str(time())[:10] + ".csv"
    xgb.baseline_learn(users, items,
                       data_interactions, 
                       target_users, target_items, result_name)
    
    # Calculate Score
    total_score = 0
    for line in open(result_name):
        # Parse line into id's wiht suers as sets for quick compare
        result = line.strip().split("\t")
        item = int(rec[0])
        rec = rec[1].split(", ")
        for user in rec:
            user = int(user)
        rec = set(rec)


        item_score = 0
        event_score = 0
        premium = 0
        paid = 0

        for key, value in target_interactions:
            if value.item.id == item:
                if value.user.id in rec:
                    if value.interaction_type == 1:
                                                
                    if value.interaction_type == 2:
                    if value.interaction_type == 5:
                    if value.interaction_type == 4:

def user_success()
"""

if __name__ == "__main__":
    run()
