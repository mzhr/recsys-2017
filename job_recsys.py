#!/usr/bin/env python3


from baseline import learner

import argparse
import time

def run():
    argparser = argparse.ArgumentParser(description='')
    argparser.add_argument("data_directory",
        help="""Location of User.csv, Items.csv, Interactions.csv,
                TargetItems.csv and TargetUsers.csv""")
    argparser.add_argument("-f", "--xfold",
        type=int,
        help="Value from 1-9 for cross validation of data.")
    argparser.add_argument("-n", "--name",
        default="submit" + str(time.time())[:10] + ".csv",
        help="Name for recommender file.")
    args = argparser.parse_args()

    start_time = time.time()

    (users, items, 
     interactions, 
     target_users, 
     target_items,
     user_cw, item_cw) = learner.baseline_parse(args.data_directory)
    if args.xfold is None:
        bst = learner.baseline_learn(users, items, interactions, target_users, target_items, user_cw, item_cw)
        learner.baseline_predict(users, items, target_users, target_items, bst, args.name, user_cw, item_cw)
#    else:
#        cross_validate.fold10(interactions, args.xfold)

    print("--- RecSys Time: %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    run()
