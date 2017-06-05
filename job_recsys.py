#!/usr/bin/env python3

"""
MAZHAR STUFF
"""

import argparse
from baseline import xgb, model
import cross_validate
import csv
import time

def run():
    """
    Gets Directory from commandline options and starts the xgboost 
    baseline learning algorithm.
    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("data_directory",
        help="""Location of User.csv, Items.csv, Interactions.csv,
                TargetItems.csv and TargetUsers.csv""")
    parser.add_argument("-f", "--xfold",
        type=int,
        help="Value from 1-9 for cross validation of data.")
    parser.add_argument("-n", "--name",
        default="submit" + str(time.time())[:10] + ".csv",
        help="Name for recommender file.")
    args = parser.parse_args()

    start_time = time.time()

    (users, items, 
     interactions, 
     target_users, 
     target_items) = xgb.baseline_parse(args.data_directory)
    if args.xfold == None:
        xgb.baseline_learn(users, items, interactions, target_users, target_items, args.name)
    else:
        cross_validate.fold10(interactions, args.xfold)

    print("--- RecSys Time: %s seconds ---" % (time.time() - start_time))


def test_score(interactions, test_location):
    with open(test_location, 'w', newline='') as csvfile:
        field_names = ['useritem', 'label', 'features', 'interactions']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for key, value in interactions.items():
            i = ""
            for inter in value.interactions:
                i += str(inter.i_type) + " "
            writer.writerow({'useritem': str(key), 'label': str(value.label()), 'features': str(value.features()), 'interactions': i})


if __name__ == "__main__":
    run()
